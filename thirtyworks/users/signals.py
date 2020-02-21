from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile


'''
want to get a post save signal when user is created
'''

# when a user is saved, then send this signal...
# sender us User
# receiver is this create_userprofile() method
@receiver(post_save, sender=User)
def create_userprofile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_userprofile(sender, instance,**kwargs):
    instance.userprofile.save()