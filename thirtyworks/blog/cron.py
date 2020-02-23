import kronos
import random
from .models import Day

@kronos.register('0 0 * * *')
def complain():
    latest_day = Day.objects.last()
    day_number = latest_day.number + 1
    day = Day(number=day_number)
    day.save()
    complaints = [
        "I forgot to migrate our applications's cron jobs to our new server! Darn!",
        "I'm out of complaints! Damnit!"
    ]

    print(random.choice(complaints))

#  python manage.py installtasks