# portal/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

# --- 1. Custom User Model (Fixes E304 Clashes) ---

class CustomUser(AbstractUser):
    """
    Defines the custom user model for the application.
    Inherits from AbstractUser to keep standard fields (username, password, etc.).
    """
    
    # Example custom field (optional, you can remove or modify)
    # phone_number = models.CharField(max_length=15, blank=True, null=True)

    # --- CRITICAL FIX for Reverse Accessor Clashes (E304) ---
    # These fields override the default AbstractUser fields to provide unique related names.
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups', # <-- Unique name for CustomUser groups
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions', # <-- Unique name for CustomUser permissions
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    # --- END CRITICAL FIX ---
    
    def __str__(self):
        return self.username


# --- 2. Resource Model (Fixes ImportError and includes the 'url' field) ---

class Resource(models.Model):
    """
    Model for storing projects or programs.
    """
    RESOURCE_CHOICES = [
        ('PROJECT', 'Project'),
        ('PROGRAM', 'Program'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    # This is the field that caused the previous FieldError in the form
    url = models.URLField(max_length=200, blank=True, null=True) 
    resource_type = models.CharField(max_length=10, choices=RESOURCE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    # Link the resource to the CustomUser
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Resources"