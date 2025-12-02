from django.shortcuts import render, redirect
from django.conf import settings
import random
from .forms import RegisterForm, LoginForm 
import time
from .models import CustomUser
from django.contrib.auth import login as auth_login, logout as auth_logout


def home(request):
    username = request.session.get("username")
    timestamp = request.session.get("timestamp")
    if request.user.is_authenticated:
        username = request.user.username
        return(render(request, "tips/home.html", {"username": username, "auth_pages": False}))
    elif not username or not timestamp or (time.time() - timestamp > 42):
        username = random.choice(settings.USERNAME_LIST)
        request.session["username"] = username
        request.session["timestamp"] = time.time()
    return(render(request, "tips/home.html", {"username": username, "auth_pages": True}))

def login(request):
    if request.method == "POST":
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

        auth_login(request, user)
        return redirect('/')
    else:
        form = LoginForm()
        
    return(render(request, "tips/login.html", {"username": "test-user", "form":form}))

def registration(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return(render(request, "tips/registration.html", {"username": "test-user", "form":form}))

def logout(request):
    auth_logout(request)
    return (redirect('/'))
    