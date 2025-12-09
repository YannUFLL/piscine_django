from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Article, UserFavouriteArticle
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    RedirectView,
    FormView,
)
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.urls import reverse_lazy



# Create your views here.
class ArticlesListView(ListView):
    model = Article
    template_name = "articles.html"
    context_object_name = "articles"

class HomeRedirectView(RedirectView):
    pattern_name = "articles"

class LogoutView(RedirectView):
    pattern_name = "articles"

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)

class AddFavouriteView(LoginRequiredMixin, RedirectView):
    pattern_name = "favourites"

    def get_redirect_url(self, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs["pk"])

        UserFavouriteArticle.objects.get_or_create(
            user=self.request.user,
            article=article
        )

        return super().get_redirect_url(*args)

class FavouritesView(LoginRequiredMixin, ListView):
    model = UserFavouriteArticle
    template_name = "favourites.html"
    context_object_name = "articles"
    def get_queryset(self):
        return  Article.objects.filter(userfavouritearticle__user=self.request.user)

class PublishView(CreateView):
    model = Article
    template_name = "publish.html"
    fields = ["title", "synopsis", "content"]
    success_url = reverse_lazy("articles")
    def form_valid(self, form):
        form.instance.author =  self.request.user
        return super().form_valid(form)
    

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

class RegisterView(CreateView):
    template_name = "register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)

        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]

        user = authenticate(self.request, username=username, password=password)

        login(self.request, user)

        return response

class LoginView(FormView):
    template_name = "login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)