from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from embed_video.fields import EmbedVideoField

class Day(models.Model):
    number = models.IntegerField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return (str(self.number))

class Post(models.Model):
    title = models.CharField(max_length=100)
    # for now let's just have text posts
    url = models.CharField(max_length=100, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    postpic = models.ImageField( upload_to='post_pics',blank=True, null=True)
    postvideo = EmbedVideoField(blank=True, null=True)
    alt_text = models.CharField(max_length=250, default=None, null=True)
    is_private = models.BooleanField(default=False)


    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk})