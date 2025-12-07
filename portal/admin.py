from django.contrib import admin
from .models import ProjectIdea, CompanyProgram

# This tells Django: "Show these tables in the Admin Panel"
admin.site.register(ProjectIdea)
admin.site.register(CompanyProgram)

# Register your models here.
