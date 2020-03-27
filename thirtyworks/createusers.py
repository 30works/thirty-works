"""

Usage: $ python manage.py shell < createusers.py

"""


from django.contrib.auth.models import User
import pandas as pd
import os
from django.db.utils import IntegrityError


EVENTBRITE_EXCEL_PATH = os.path.join(os.path.expanduser('~'), 'eventbrite_data_dummy.xlsx')

def id_generator(size):
    import random
    import string
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))

# read the CSV file
# df = pd.read_csv(USER_DATA_PATH)
# read the Excel file
df = pd.read_excel(EVENTBRITE_EXCEL_PATH)

for i, row in df.iterrows():
    username = row['First Name'] + '_' + row['Surname']
    email_address = row['Email Address']
    password = id_generator(10)
    try:
        user = User.objects.create_user(username=username, password=password, email=email_address)
        user.is_superuser = False
        user.is_staff = False
        user.save()

        print('Created User: {}\nEmail: {}\nPass: {}\n=========='.format(username, email_address, password))
    except IntegrityError as ie:
        print(ie)
        print('Couldnt create User: {}\nEmail: {}\nPass: {}\n=========='.format(username, email_address, password))
