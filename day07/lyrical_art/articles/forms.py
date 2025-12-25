from django.contrib.auth.forms import  AuthenticationForm, UsernameField
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import UserFavouriteArticle


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True, "class":"form-control form-control-sm", "placeholder":_("Username")}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "class":"form-control form-control-sm", "placeholder":_("Password")}))

class AddToFavouriteForm(forms.ModelForm):
    class Meta:
        model = UserFavouriteArticle
        fields = []