from django.db import models
from django.contrib.auth.models import User

# --- 1. Resources Model ---
class Resource(models.Model):
    """Model to store learning resources, project ideas, and company programs."""

    RESOURCE_CHOICES = [
        ('PROJECT', 'Project Idea'),
        ('PROGRAM', 'Company Program'),
        ('ARTICLE', 'Article/Tutorial'),
        ('VIDEO', 'Video Link'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(max_length=200, blank=True, null=True)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE) 

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_resource_type_display()}] {self.title}"


# --- 2. Company Programs Model (THIS IS THE MISSING CLASS) ---
class CompanyProgram(models.Model):
    """Model to store details about company-specific programs, like internships or challenges."""
    
    PROGRAM_CHOICES = [
        ('INTERNSHIP', 'Internship/Fellowship'),
        ('CONTEST', 'Coding Contest/Challenge'),
        ('TRAINING', 'Training/Bootcamp'),
        ('OTHER', 'Other Program'),
    ]

    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=100)
    description = models.TextField()
    program_type = models.CharField(max_length=20, choices=PROGRAM_CHOICES)
    link = models.URLField(max_length=200)
    deadline = models.DateField(blank=True, null=True) 
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Company Programs"

    def __str__(self):
        return f"{self.company_name}: {self.title}"