from django.contrib.auth.models import User
import pandas as pd
import os
# import random
# import string


def id_generator(size):
    import random
    import string
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))

USER_DATA_PATH = os.path.join(os.path.expanduser('~'), 'eventbrite_data_dummy.xlsx')

# read the CSV file
# df = pd.read_csv(USER_DATA_PATH)
df = pd.read_excel(USER_DATA_PATH)

for i, row in df.iterrows():
    username = row['First Name'] + '_' + row['Surname']
    email_address = row['Email Address']
    password = id_generator(10)

    user = User.objects.create_user(username=username, password=password, email=email_address)
    user.is_superuser = False
    user.is_staff = False
    user.save()

    print('Created User: {}\nEmail: {}\nPass: {}\n=========='.format(username, email_address, password))
