
# portal/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Authentication paths
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    # Core Application Paths
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('resources/', views.resources_view, name='resources'),
]