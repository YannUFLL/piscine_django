from django.urls import path
from . import views

urlpatterns = [
    path('', views.account_page),
    path('login/', views.ajax_login),
    path('logout/', views.ajax_logout)
]