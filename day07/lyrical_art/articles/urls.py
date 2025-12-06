from django.urls import path
from . import views

urlpatterns = [
path('', views.HomeRedirectView.as_view(), name="home"),
path('login', views.LoginView.as_view(), name="login"),
path('logout', views.LoginView.as_view(), name="logout"),
path('articles', views.ArticlesListView.as_view(), name="articles"),
path('articles/<int:pk>/', views.ArticleDetailView.as_view(), name="article-detail"),
path('favourites', views.FavouritesView.as_view(), name="favourties")
]