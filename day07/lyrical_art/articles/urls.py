from django.urls import path
from . import views

urlpatterns = [
path('', views.HomeRedirectView.as_view(), name="home"),
path('login', views.LoginView.as_view(), name="login"),
path('logout', views.LogoutView.as_view(), name="logout"),
path('articles', views.ArticlesListView.as_view(), name="articles"),
path('articles/<int:pk>/', views.ArticleDetailView.as_view(), name="article-detail"),
path('favourites', views.FavouritesView.as_view(), name="favourites"),
path('register', views.RegisterView.as_view(), name="register"),
path('publications', views.PublicationsView.as_view(), name="publications"),
path('publish', views.PublishView.as_view(), name="publish"),
path('articles/add-favourite/<int:pk>', views.AddFavouriteView.as_view(), name="add-favourite")
]