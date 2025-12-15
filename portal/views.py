from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.cache import cache
from django.conf import settings
import logging

# --- UPDATED IMPORTS ---
from .forms import ResourceForm, LoginForm, UserRegisterForm, ProgramForm
from .models import Resource, CompanyProgram
# -----------------------

logger = logging.getLogger('portal')
MAX_LOGIN_ATTEMPTS = 5 
LOCKOUT_TIME = 300 

# ------------------------------------------------
# 1. AUTHENTICATION VIEWS (Login security FIX APPLIED)
# ------------------------------------------------

def login_view(request):
    is_locked_out = False
    lockout_time_remaining = 0
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = form['username'].value()
        cache_key = f'login_attempts_{username.lower()}'
        attempts = cache.get(cache_key, 0)

        # 1. Check for existing lock BEFORE processing
        if attempts >= MAX_LOGIN_ATTEMPTS:
            ttl = cache.ttl(cache_key) 
            
            if ttl > 0:
                is_locked_out = True
                lockout_time_remaining = ttl
                
                logger.warning(f"SECURITY: Attempted login by locked user {username}. Time remaining: {lockout_time_remaining}s")
                messages.error(request, f"Access denied. Too many failed login attempts. Account locked.")
                return render(request, 'login.html', locals()) 
            else:
                # Lockout time expired
                cache.delete(cache_key)
                attempts = 0 

        # 2. Process form submission
        if form.is_valid():
            user = authenticate(request, 
                                username=username, 
                                password=form.cleaned_data['password'])
            
            if user is not None:
                login(request, user)
                
                # Successful login: clear any failed attempts from cache
                if attempts > 0:
                    cache.delete(cache_key)
                    logger.info(f"SUCCESS: User {username} logged in successfully. Attempts cleared.")
                
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                # Failed login attempt (user is None)
                
                new_attempts = 0 
                
                # Update attempts count
                if attempts == 0:
                    cache.set(cache_key, 1, timeout=LOCKOUT_TIME)
                    new_attempts = 1
                else:
                    new_attempts = cache.incr(cache_key, delta=1)
                
                
                # Check for lockout after updating count
                if new_attempts >= MAX_LOGIN_ATTEMPTS:
                    
                    # FIX for AttributeError: Replaced cache.expire with cache.set
                    cache.set(cache_key, MAX_LOGIN_ATTEMPTS, timeout=LOCKOUT_TIME)
                    
                    is_locked_out = True
                    lockout_time_remaining = LOCKOUT_TIME
                    
                    logger.error(f"LOCKOUT: User {username} locked out for {LOCKOUT_TIME}s after {new_attempts} failed attempts.")
                    messages.error(request, f"Access denied. Too many failed login attempts. Account locked.")
                else:
                    attempts_left = MAX_LOGIN_ATTEMPTS - new_attempts
                    messages.warning(request, f"Invalid username or password. {attempts_left} attempts remaining.")
                
        else:
            messages.error(request, "Please enter both username and password.")

    context = {
        'form': form,
        'is_locked_out': is_locked_out,
        'lockout_time_remaining': lockout_time_remaining,
    }
    return render(request, 'login.html', context)


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) 
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
        else:
            pass 
    else:
        form = UserRegisterForm()
        
    context = {'form': form}
    return render(request, 'register.html', context)


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


# ------------------------------------------------
# 2. APPLICATION VIEWS
# ------------------------------------------------

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')


@login_required
def resources_view(request):
    form = ResourceForm()

    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            new_resource = form.save(commit=False)
            new_resource.created_by = request.user
            new_resource.save()
            messages.success(request, f"Resource '{new_resource.title}' added successfully!")
            return redirect('resources')
        else:
            messages.error(request, "Failed to add resource. Please check the form.")

    resources = Resource.objects.all().order_by('-created_at')
    
    context = {
        'form': form,
        'resource_groups': {
            'Project Ideas': resources.filter(resource_type='PROJECT'),
            'Company Programs': resources.filter(resource_type='PROGRAM'),
            'Articles/Tutorials': resources.filter(resource_type='ARTICLE'),
            'Video Links': resources.filter(resource_type='VIDEO'),
        }
    }
    return render(request, 'resources.html', context)


@login_required
def programs_view(request):
    """
    Handles creation and display of company programs, grouped by type.
    """
    form = ProgramForm()

    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            new_program = form.save(commit=False)
            new_program.created_by = request.user
            new_program.save()
            messages.success(request, f"Program '{new_program.title}' for {new_program.company_name} added successfully!")
            return redirect('programs')
        else:
            messages.error(request, "Failed to add program. Please check the form.")

    programs = CompanyProgram.objects.all().order_by('-created_at')
    
    context = {
        'form': form,
        'program_groups': {
            'Internships & Fellowships': programs.filter(program_type='INTERNSHIP'),
            'Coding Contests & Challenges': programs.filter(program_type='CONTEST'),
            'Training & Bootcamps': programs.filter(program_type='TRAINING'),
            'Other Programs': programs.filter(program_type='OTHER'),
        }
    }
    return render(request, 'programs.html', context)


@login_required
def projects_view(request):
    """
    Displays Project Ideas submitted by users, using the Resource model, filtered for 'PROJECT'.
    """
    # Filter the Resource model to only show items where resource_type is 'PROJECT'
    projects = Resource.objects.filter(resource_type='PROJECT').order_by('-created_at')

    context = {
        'projects': projects,
    }
    return render(request, 'projects.html', context)