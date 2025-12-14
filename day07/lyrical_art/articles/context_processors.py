from .forms import CustomAuthenticationForm

def login_form(request):
    return {"menu_login_form": CustomAuthenticationForm(request=request)}
