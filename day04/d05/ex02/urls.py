from django.urls import path
from . import views

app_name = "ex02"

urlpatterns = [ 
    path("", views.form_view, name="ex02"),
]