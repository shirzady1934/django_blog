from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    title = models.CharField(max_length = 250)
    text = models.TextField()
    created_date = models.DateField(default = timezone.now) 
    published_date = models.DateTimeField(blank=True, null=True)
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    def __str__(self):
        return self.title
class Token(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    token = models.CharField(max_length = 20)
    def __str__(self):
        return self.token
