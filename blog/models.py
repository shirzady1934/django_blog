from django.db import models
from django.utils import timezone
from django.conf import settings
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    title = models.CharField(max_length = 250)
    text = models.TextField()
    created_date = models.DateField(default = timezone.now())
    publishied_date = models.DateTimeField(default = timezone.now())
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    def __str__(self):
        return self.title
