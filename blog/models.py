from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
class Post(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 250)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now) 
    def __str__(self):
        return self.title
class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length = 20)
    def __str__(self):
        return self.token
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    age = models.IntegerField()
    location = models.CharField(max_length=20)
    def __str__(self):
        return self.user.username
