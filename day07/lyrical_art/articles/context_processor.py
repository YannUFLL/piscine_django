from django.contrib.auth.forms import AuthenticationForm

def login_form(request):
    return {"menu_login_form": AuthenticationForm(request=request)}
