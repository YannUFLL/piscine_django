from django.shortcuts import render, redirect
from django.conf import settings
import random
from .forms import RegisterForm, LoginForm,  TipForm
import time
from .models import CustomUser, Tip
from django.contrib.auth import login as auth_login, logout as auth_logout


def home(request):
    username = request.session.get("username")
    timestamp = request.session.get("timestamp")
    tips = Tip.objects.order_by("date")
    reputation = 0
    if request.user.is_authenticated:
        reputation = request.user.reputation
        tipform = TipForm()
        username = request.user.username
        return(render(request, "tips/home.html", {"username": username, "auth_pages": False, "tipform": tipform, "tips":tips, "reputation":reputation}))
    elif not username or not timestamp or (time.time() - timestamp > 42):
        username = random.choice(settings.USERNAME_LIST)
        request.session["username"] = username
        request.session["timestamp"] = time.time()
    return(render(request, "tips/home.html", {"username": username, "auth_pages": True, "tips": tips}))


def addtip(request):
    print("USER AUTHENTICATED")
    if request.user.is_authenticated:
        print("USER AUTHENTICATED")
        tipform = TipForm(request.POST)
        if tipform.is_valid():
            tip = tipform.save(commit=False)
            tip.author = request.user
            tip.save()
    return (redirect('/'))

def deltip(request):
    if request.user.is_authenticated:
        tip = Tip.objects.filter(id=request.POST.get("tip_id")).first()
        if tip.author == request.user or request.user.has_perm("tips.delete_tip") or request.user.can_delete_tips() :
            author = tip.author
            author.reputation -= (tip.upvotes.count() * 5)
            author.reputation += (tip.downvotes.count() * 2)
            author.save()
            tip.delete()
    return (redirect('/'))


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

def downvotetip(request):
    if request.user.is_authenticated:
        user = request.user
        tip = Tip.objects.filter(id=request.POST.get("tip_id")).first()
        if tip and (request.user.has_perm("tips.candownvote") or user == tip.author or user.can_downvote()):
            if user in tip.upvotes.all():
                tip.upvotes.remove(user)
                tip.author.reputation -= 5
                tip.author.save()
            if user in tip.downvotes.all():
                tip.downvotes.remove(user)
                tip.author.reputation += 2
                tip.author.save()
            else:
                tip.author.reputation -= 2
                tip.downvotes.add(user)
                tip.author.save()
    return (redirect('/'))

def upvotetip(request):
    if request.user.is_authenticated:
        tip = Tip.objects.filter(id=request.POST.get("tip_id")).first()
        if tip:
            user = request.user
            if user in tip.downvotes.all():
                tip.downvotes.remove(user)
                tip.author.reputation += 2
                tip.author.save()
            if user in tip.upvotes.all():
                tip.upvotes.remove(user)
                tip.author.reputation -= 5
                tip.author.save()
            else:
                tip.author.reputation += 5
                tip.upvotes.add(user)
                tip.author.save()
    return (redirect('/'))


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
    