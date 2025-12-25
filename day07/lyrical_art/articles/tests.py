from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Article
from .models import UserFavouriteArticle

class ExampleTests(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="yann",
            password="pass1234"
        )

    def test_requires_login(self):
        response = self.client.get(reverse("favourites"))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse("publications"))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse("publish"))
        self.assertEqual(response.status_code, 302)
        self.client.login(username="yann", password="pass1234")
        response = self.client.get(reverse("favourites"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("publications"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("publish"))
        self.assertEqual(response.status_code, 200)

    def test_requires_logout(self):
        self.client.login(username="yann", password="pass1234")
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 302)

    def test_add_favourites_twice(self):
        self.client.login(username="yann", password="pass1234")
        article = Article.objects.create(title="test", author=self.user, synopsis="test", content="lol")
        self.client.post(reverse('add-favourite', kwargs={ "pk": article.pk}))
        self.assertEqual(UserFavouriteArticle.objects.count(), 1)
        self.client.post(reverse('add-favourite', kwargs={ "pk": article.pk}))
        self.assertEqual(UserFavouriteArticle.objects.count(), 1)
