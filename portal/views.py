
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import ProjectIdea, CompanyProgram
from .forms import LoginForm, RegisterForm, ProjectForm, ProgramForm

# --- PROTECTED PAGES ---

@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'dashboard.html')

@login_required(login_url='login')
def resources_view(request):
    projects = ProjectIdea.objects.all()
    programs = CompanyProgram.objects.all()
    context = {'projects': projects, 'programs': programs}
    return render(request, 'resources.html', context)

# --- PROJECT FEATURES ---

@login_required(login_url='login')
def add_project_view(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('resources')
    else:
        form = ProjectForm()
    return render(request, 'add_project.html', {'form': form})

@login_required(login_url='login')
def edit_project_view(request, project_id):
    project = get_object_or_404(ProjectIdea, id=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('resources')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'edit_project.html', {'form': form})

@login_required(login_url='login')
def delete_project_view(request, project_id):
    project = get_object_or_404(ProjectIdea, id=project_id)
    project.delete()
    return redirect('resources')

# --- HIRING PROGRAM FEATURES ---

@login_required(login_url='login')
def add_program_view(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('resources')
    else:
        form = ProgramForm()
    return render(request, 'add_program.html', {'form': form})

@login_required(login_url='login')
def delete_program_view(request, program_id):
    program = get_object_or_404(CompanyProgram, id=program_id)
    program.delete()
    return redirect('resources')

# --- AUTHENTICATION ---

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')