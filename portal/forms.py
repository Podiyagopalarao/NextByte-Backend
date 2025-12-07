from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import ProjectIdea, CompanyProgram  # <--- Added CompanyProgram

# 1. Login Form
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

# 2. Register Form
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

# 3. Project Form
class ProjectForm(forms.ModelForm):
    class Meta:
        model = ProjectIdea
        fields = ['title', 'domain', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Project Title'}),
            'domain': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Domain (e.g. AI, Web)'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

# 4. Program Form (NEW!)
class ProgramForm(forms.ModelForm):
    class Meta:
        model = CompanyProgram
        fields = ['company_name', 'program_name', 'eligibility_criteria']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name (e.g. Google)'}),
            'program_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Program Name (e.g. Summer Intern)'}),
            'eligibility_criteria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Who can apply?'}),
        }