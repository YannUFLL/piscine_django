from django.urls import path
from . import views

urlpatterns = [
path('', views.HomeRedirectView.as_view(), name="home"),
path('login', views.LoginView.as_view(), name="login"),
path('articles', views.ArticlesListView.as_view(), name="articles")
]