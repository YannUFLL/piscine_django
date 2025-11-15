from django.urls import path
from . import views

app_name = "ex02"

urlpatterns = [ 
    path("init", views.init, name="ex02"),
    path("populate", views.populate, name="ex02"),
    path("display", views.display, name="ex02"),
]