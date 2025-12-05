from django.shortcuts import render
from .models import Article
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

class LoginView(FormView):
    template_name = "login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)