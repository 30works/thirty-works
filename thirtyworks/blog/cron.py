import kronos
import random
from blog.models import Day, Post
from users.models import UserProfile
from django.core.mail import send_mail
from django.conf import settings
import os
import json


with open(os.path.join(os.path.expanduser('~'), '30works.json'), 'r') as f:
    config_json = json.load(f)

DAILY_BRIEF_EMAIL = """

day {} brief

deadline: 23:59 * today ({}th)

brief :  {}

Submit your work today through the thirty.works portal  link here   (submit button is in the top right corner) 

*this is london, UK time (GMT+1:00 or BST)


12ø xx

"""

COMMISERATIONS_EMAIL = """

oh nooooo . . . . . .

we're sad to see you go !

We didn't get your work in time for the deadline yesterday, this means that unfortunately you are no longer able to participate in the project.

Check out thirty.works and our instagram, twitter and facebook for a selection of works submitted each day!

We hope to see you participate in other future projects - sign up to be on our mailing list through our website and keep in touch!


12ø xx


"""

def email(subject, message, recipient_list):
    email_from = settings.EMAIL_HOST_USER
    send_mail( subject, message, email_from, recipient_list )

@kronos.register('15 15 * * *') # currently set to 3:30 PM for testing
def complain():
    rejected_users = []
    accepted_users = []
    latest_day = Day.objects.last()
    posts = Post.objects.filter(day=latest_day)
    authors_who_submitted_today = []
    for post in posts:
        authors_who_submitted_today.append(post.author.username)
    users = UserProfile.objects.all()
    print(authors_who_submitted_today)
    for user in users:
        if user.user.is_active and not user.user.is_staff:
            if user.user.username not in authors_who_submitted_today:
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

    # accepted_subject = "Accepted."
    accepted_subject = "30/30 Day {}".format(day_number)
    accepted_message = "{}".format(DAILY_BRIEF_EMAIL)
    accepted_message = accepted_message.format(day_number, day_number)

    # rejected_subject = "Rejected."
    rejected_subject = "30/30 - oh noo, our commiserations"
    # rejected_message = "You are being blocked to use the system."
    rejected_message = "{}".format(COMMISERATIONS_EMAIL)
    brief = config_json[str(latest_day.number)]
    rejected_message = rejected_message.format(brief)

    # debugging
    # print(accepted_users)
    # print(rejected_users)
    print('accept message: ')
    print(accepted_message)
    print('reject message: ')
    print(rejected_message)

    email(rejected_subject, rejected_message, rejected_users)
    print("Email has been sent to rejected users.")
    email(accepted_subject, accepted_message, accepted_users)
    print("Email has been sent to active users.")

# python manage.py installtasks
# python manage.py showtasks