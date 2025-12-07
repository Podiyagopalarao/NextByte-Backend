
from django.db import models
from django.contrib.auth.models import User

# 1. Table for Student Projects
class ProjectIdea(models.Model):
    title = models.CharField(max_length=200)
    domain = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title

# 2. Table for Hiring Programs (This was causing the error!)
class CompanyProgram(models.Model):
    # These names MUST match what is in forms.py
    company_name = models.CharField(max_length=200)
    program_name = models.CharField(max_length=200)
    eligibility_criteria = models.TextField()

    def __str__(self):
        return self.program_name