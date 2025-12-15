# portal/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from django.core.cache import cache 
from functools import wraps 
import logging 

# --- Constants for Security ---
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_TIME = 300 # 5 minutes in seconds
# -----------------------------

from .forms import ResourceForm, LoginForm, CustomUserCreationForm 
from .models import Resource 

logger = logging.getLogger('portal')


# --- Rate Limiting Decorator (Unchanged) ---

def rate_limit(limit, period):
    """Decorator to limit requests by authenticated user ID."""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                cache_key = f"rate_limit:{request.user.id}:{view_func.__name__}"
                hits = cache.get(cache_key, 0) + 1
                
                if hits > limit:
                    logger.warning(f"Rate limit exceeded for user: {request.user.username} on view: {view_func.__name__}") 
                    return render(request, '429_ratelimit.html', status=429) 
                
                cache.set(cache_key, hits, period)
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


# --- Authentication Views ---

def login_view(request):
    """
    Handles login and implements a brute-force prevention mechanism.
    Checks cache on GET/initial load to persist lockout status and calculates remaining time.
    """
    form = LoginForm() 
    username = request.POST.get('username', '')
    is_locked_out = False
    lockout_time_remaining = 0  # Time in seconds remaining for countdown
    minutes = LOCKOUT_TIME // 60 
    
    # Check current attempts for persistence (based on form data or default empty string)
    cache_key = f"login_failed:{username}"
    attempts = cache.get(cache_key, 0)
    
    # 1. PERSISTENCE CHECK: Check if the key exists AND if the lockout limit is met
    if attempts >= MAX_LOGIN_ATTEMPTS:
        ttl = cache.ttl(cache_key) # Get remaining time in seconds
        
        if ttl > 0:
            is_locked_out = True
            lockout_time_remaining = ttl
            # Set message for persistence on page load
            messages.error(request, f"Access denied. Too many failed login attempts. Account locked.")
    
    # --- Start POST handling ---
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST) 
        username = request.POST.get('username') # Get the actual posted username
        
        # Recalculate cache key for the posted username
        cache_key = f"login_failed:{username}"
        attempts = cache.get(cache_key, 0)

        # 2. Check if the user is currently locked out based on the submitted username
        if attempts >= MAX_LOGIN_ATTEMPTS:
            is_locked_out = True
            # Get TTL for the submitted username if they try while already locked out
            lockout_time_remaining = cache.ttl(cache_key) 
            messages.error(request, f"Access denied. Too many failed login attempts. Account locked.")
            logger.warning(f"Access denied for user {username}: Locked out for {LOCKOUT_TIME} seconds.")
            # Do NOT continue to validation if locked out

        # 3. Process authentication only if NOT locked out AND form is valid
        elif form.is_valid():
            user = form.get_user() 
            
            login(request, user)
            logger.info(f"User login successful: {user.username}") 
            messages.success(request, f"Welcome back, {user.username}!")
            
            # Reset attempts on success
            cache.delete(cache_key)
            
            return redirect('dashboard')
        
        # 4. Process a new failed login attempt (i.e., wrong credentials, and not yet locked out)
        else:
            logger.warning(f"Failed login attempt for user: {username}.") 
            
            # Increment failed attempts and set/reset the expiration time
            try:
                new_attempts = cache.incr(cache_key, delta=1)
            except ValueError:
                cache.set(cache_key, 1, LOCKOUT_TIME)
                new_attempts = 1
                
            # Check immediately if this failure triggers the lockout
            if new_attempts >= MAX_LOGIN_ATTEMPTS:
                is_locked_out = True 
                lockout_time_remaining = LOCKOUT_TIME # Set full lockout time
                messages.error(request, f"Access denied. Too many failed login attempts. Account locked.")
            else:
                remaining = MAX_LOGIN_ATTEMPTS - new_attempts
                messages.error(request, f"Authentication failed. Check your credentials. You have {remaining} attempts remaining.")
                
    # Final render, pass the form, the lockout flag, and the time remaining
    context = {
        'form': form,
        'is_locked_out': is_locked_out,
        'lockout_time_remaining': lockout_time_remaining 
    }
    return render(request, 'login.html', context) 


def logout_view(request):
    """Logs the user out and redirects to the login page."""
    if request.user.is_authenticated:
        logger.info(f"User logout successful: {request.user.username}") 
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login') 


def register_view(request):
    """
    Handles new user registration using the fixed CustomUserCreationForm.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST) 
        if form.is_valid():
            user = form.save() 
            login(request, user)
            logger.info(f"New user registered and logged in: {user.username}")
            messages.success(request, f"Account created and logged in successfully!")
            return redirect('dashboard')
        else:
            # Display detailed form errors
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'register.html', {'form': form})


# --- Core Application Views (Unchanged) ---

@login_required 
@rate_limit(limit=10, period=60) 
def dashboard_view(request):
    """Displays the user's dashboard (Feature A1)."""
    return render(request, 'dashboard.html')


@login_required 
def resources_view(request):
    """Handles adding and displaying resources."""
    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            new_resource = form.save(commit=False)
            new_resource.created_by = request.user 
            new_resource.save()
            logger.info(f"Resource added by {request.user.username}: {new_resource.title} ({new_resource.resource_type})") 
            messages.success(request, f"{new_resource.resource_type} '{new_resource.title}' added successfully!")
            return redirect('resources') 
        else:
            messages.error(request, "Failed to add resource. Please check the form.")
    else:
        form = ResourceForm() 

    # Retrieve all resources for display
    projects = Resource.objects.filter(resource_type='PROJECT').order_by('-created_at')
    programs = Resource.objects.filter(resource_type='PROGRAM').order_by('-created_at')

    context = {
        'projects': projects, 
        'programs': programs,
        'form': form
    }
    return render(request, 'resources.html', context)