import kronos
import random
from blog.models import Day, Post
from users.models import UserProfile
from django.core.mail import send_mail
from django.conf import settings

def email(subject, message, recipient_list):
    email_from = settings.EMAIL_HOST_USER
    send_mail( subject, message, email_from, recipient_list )

@kronos.register('30 13 * * *')
def complain():
    rejected_users = []
    accepted_users = []
    latest_day = Day.objects.last()
    posts = Post.objects.filter(day=latest_day)
    authors = []
    for post in posts:
        authors.append(post.author.username)
    users = UserProfile.objects.all()
    print(authors)
    for user in users:
        if user.user.is_active and not user.user.is_staff:
            if user.user.username not in authors:
                rejected_users.append(user.user.email)
                user.user.is_active = False
                user.user.save()
                user.blocked = True
                user.save()
            else:
                accepted_users.append(user.user.email)
    day_number = latest_day.number + 1
    day = Day(number=day_number)
    day.save()
    accepted_subject = "Accepted."
    accepted_message = "Your task is to play."
    rejected_subject = "Rejected."
    rejected_message = "You are being blocked to use the system."
    print(accepted_users)
    print(rejected_users)
    email(rejected_subject, rejected_message, rejected_users)
    print("Email has been sent to rejected users.")
    email(accepted_subject, accepted_message, accepted_users)
    print("Email has been sent to active users.")

# python manage.py installtasks
# python manage.py showtasks