from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Create your models here.

class UserProfile(models.Model):
    '''
    Extend default model to contain profile photo
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profilepic = models.ImageField(default='default_profilepic.png', upload_to='profile_pics')
    blocked = models.BooleanField(default=False)
    insta_handler = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)
    date_blocked = models.DateField(blank=True, null=True)


    def __str__(self):
        return '{} Profile'.format(self.user.username)

    def save(self, *args, **kwargs):
        '''
        Overriding default save to implement image downsampling for disk space saving
        '''
        super().save(*args, **kwargs)

        im = Image.open(self.profilepic.path)

        if im.height > 300 or im.width > 300:
            output_size = (300,300)
            im.thumbnail(output_size)
            im.save(self.profilepic.path)