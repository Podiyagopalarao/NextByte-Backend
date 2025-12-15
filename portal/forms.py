# portal/forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm 

# --- Import your project models ---
from .models import Resource, CustomUser 


# --- Custom Registration Form (Fixed for CustomUser) ---

class CustomUserCreationForm(DjangoUserCreationForm):
    """
    Form using the CustomUser model for registration.
    """
    class Meta(DjangoUserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email') 


# --- LoginForm (Cleaned: Standard AuthenticationForm) ---

class LoginForm(AuthenticationForm):
    """
    Standard AuthenticationForm.
    """
    username = forms.CharField(max_length=254, 
                               widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label=("Password"),
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))


# --- ResourceForm (Final Version with 'url' field) ---

class ResourceForm(forms.ModelForm):
    """
    Form for adding Resources (Projects or Programs).
    """
    class Meta:
        model = Resource
        # >>> FINAL FIX: 'url' field is added back here.
        fields = ['title', 'description', 'url', 'resource_type'] 
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'url': forms.URLInput(attrs={'class': 'form-control'}), # This widget is now active
            'resource_type': forms.Select(attrs={'class': 'form-control'}),
        }