from django.shortcuts import render
from .models import Article, UserFavouriteArticle
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    RedirectView,
    FormView,
)
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy



# Create your views here.
class ArticlesListView(ListView):
    model = Article
    template_name = "articles.html"
    context_object_name = "articles"

class HomeRedirectView(RedirectView):
    pattern_name = "articles"

    from django.contrib.auth import logout
from django.views.generic import RedirectView
from django.urls import reverse_lazy

class LogoutView(RedirectView):
    patter_name = "home"

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)

class FavouritesView(LoginRequiredMixin, ListView):
    model = UserFavouriteArticle
    template_name = "favourites.html"
    context_object_name = "articles"
    def get_queryset(self):
       return  Article.objects.filter(userfavouritearticle__user=self.request.user)

class PublicationsView(LoginRequiredMixin, ListView):
    model = Article
    template_name = "publications.html"
    context_object_name = "articles"
    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)

class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = "article_detail.html"
    context_object_name="article"

class LoginView(FormView):
    template_name = "login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)