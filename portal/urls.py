# portal/urls.py 

from django.urls import path
from . import views

urlpatterns = [
    # General Pages
    path('', views.dashboard_view, name='dashboard'), 
    
    # Authentication Paths
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Application Features
    path('resources/', views.resources_view, name='resources'),
    path('programs/', views.programs_view, name='programs'),
    
    # <-- ADDED: Project Ideas Path -->
    path('projects/', views.projects_view, name='projects'), 
]