
from django.urls import path
from . import views

urlpatterns = [
    # 1. Main Pages
    path('', views.dashboard_view, name='dashboard'),
    path('resources/', views.resources_view, name='resources'),
    
    # 2. Project Features
    path('add-project/', views.add_project_view, name='add_project'),
    path('edit/<int:project_id>/', views.edit_project_view, name='edit_project'),
    path('delete/<int:project_id>/', views.delete_project_view, name='delete_project'),

    # 3. Hiring Programs
    path('add-program/', views.add_program_view, name='add_program'),
    path('delete-program/<int:program_id>/', views.delete_program_view, name='delete_program'),

    # 4. Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]