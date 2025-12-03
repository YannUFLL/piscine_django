from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    reputation = models.IntegerField(default=0)

    def __str__(self):
        return self.username
    
    def can_downvote(self):
        return self.reputation >= 15

    def can_delete_tips(self):
        return self.reputation >= 30

class Tip(models.Model):
    content = models.CharField(null=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tips")
    date = models.DateTimeField(auto_now_add=True)
    downvotes =  models.ManyToManyField(CustomUser, related_name="downvoted_tips")
    upvotes =  models.ManyToManyField(CustomUser, related_name="upvoted_tips")



    class Meta:
        permissions = [
            ("candownvote", "Can downvote tips"),
        ]