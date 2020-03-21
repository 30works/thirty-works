# 30 days 30 works website

## Main installation instructions

* Clone repo
* Create a virtualenv with required dependencies
* Delete any existing database files
* `$ python manage.py migrate`  to create database tables
* `$ python manage.py createsuperuser` and log in to create the first Day in the admin backend
* `$ python manage.py installtasks` to configure the daily cron job (emails and day increment)
* `$ python manage.py collectstatic` to collect all static files

Website is now ready to serve