from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def account_page(request):
    form = AuthenticationForm(request)
    return render(request, "account/account.html", {"form": form})

@require_POST
def ajax_login(request):
    if request.user.is_authenticated:
        return JsonResponse({"ok": True, "username":request.user.get_username()})
    
    form = AuthenticationForm(request, data=request.POST)
    if (form.is_valid()):
        print(login)
        login(request, form.get_user())
        return JsonResponse({"ok": True, "username": form.get_user().get_username()})

    return JsonResponse({"ok": False, "errors": form.errors}, status=400)

@require_POST
def ajax_logout(request):
    logout(request)
    return JsonResponse({"ok": True})