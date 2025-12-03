from django.urls import path
from . import views

urlpatterns = [path("", views.home),
                path("login", views.login),
                path("register", views.registration),
                path("logout", views.logout),
                path("addtip", views.addtip),
                path("deltip", views.deltip),
                path("upvotetip", views.upvotetip),
                path("downvotetip", views.downvotetip)
                ]