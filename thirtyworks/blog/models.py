from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from embed_video.fields import EmbedVideoField
import copy
from PIL import Image
from django.core.exceptions import ValidationError



def resize_to_maxsize(max_size, pil_image):
    width, height = pil_image.size

    # if the image exceeds maximum size
    if height > max_size or width > max_size:

        new_width, new_height = copy.deepcopy(width), copy.deepcopy(height)

        # if portrait
        if height > width:
            new_width = max_size * (width / float(height))
        # if landscape
        else:
            new_height = max_size * (height / float(width))

        pil_image.thumbnail((new_width, new_height), Image.ANTIALIAS)

    return pil_image


class Day(models.Model):
    number = models.IntegerField(verbose_name="Day Number")
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return (str(self.number))

class Post(models.Model):
    title = models.CharField(max_length=100)
    datetime_posted = models.DateTimeField(default=timezone.now)

    url = models.CharField(max_length=250, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    postpic = models.ImageField( upload_to='post_pics',blank=True, null=True)
    postvideo = EmbedVideoField(blank=True, null=True)
    alt_text = models.CharField(max_length=250, default=None, null=True)
    is_private = models.BooleanField(default=False)
    anything_else = models.CharField(max_length=250, default=None, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk})
    
    def __str__(self):
        return ("Post " + str(self.id) + " " + str(self.title))

    def save(self, *args, **kwargs):
        '''
        Overriding default save to implement image downsampling for disk space saving
        '''
        super().save(*args, **kwargs)


        # set maximum allowed image size
        MAX_SIZE = 900

        # if the post is a picture upload
        if self.postpic:

            # open the image
            im = Image.open(self.postpic.path)

            # resize if necessary
            im = resize_to_maxsize(MAX_SIZE, im)

            # save the image file
            im.save(self.postpic.path)


    def clean(self):
        if (not self.postpic) and (not self.url) and (not self.postvideo):
        # if not self.postpic or self.url or self.postvideo:
            raise ValidationError("You must specify an image to upload, a webpage URL, or a soundcloud/youtube/vimeo link")
        super().clean()