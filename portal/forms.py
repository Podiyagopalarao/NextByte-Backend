from django import forms
# Ensure both models are imported
from .models import Resource, CompanyProgram 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# 1. Login Form
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


# 2. Registration Form
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields


# 3. Resource Form
class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'description', 'url', 'resource_type']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'resource_type': forms.Select(attrs={'class': 'form-select'}),
        }


# 4. Program Form (THIS IS THE MISSING CLASS)
class ProgramForm(forms.ModelForm):
    deadline = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Application Deadline (Optional)'
    )

    class Meta:
        model = CompanyProgram
        fields = ['title', 'company_name', 'description', 'program_type', 'link', 'deadline']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'program_type': forms.Select(attrs={'class': 'form-select'}),
            'link': forms.URLInput(attrs={'class': 'form-control'}),
        }