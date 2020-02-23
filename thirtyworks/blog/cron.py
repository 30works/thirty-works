import kronos
import random
from .models import Day

@kronos.register('0 0 * * *')
def complain():
    day = Day(number=29)
    day.save()
    complaints = [
        "I forgot to migrate our applications's cron jobs to our new server! Darn!",
        "I'm out of complaints! Damnit!"
    ]

    print(random.choice(complaints))

#  python manage.py installtasks