
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    username = forms.CharField(label="Username",
                                max_length=150,
                                widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Enter a unique username", "autocomplete":"username"}))
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder":"Enter a password", "autocomplete":"new-password"}))
    password2 = forms.CharField(label="Confirm Password",
                                widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder":"Re-enter password", "autocomplete":"new-password"}))
    class Meta:
        model = CustomUser
        fields = ["username", "password1", "password2"]


class LoginForm(AuthenticationForm):
        
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'})
    )
    
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )