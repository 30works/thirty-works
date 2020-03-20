"""
WSGI config for thirtyworks project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
import sys

# add the thirtyworks project path into the sys.path
sys.path.append('/home/ubuntu/thirty-works/thirtyworks')

# add the virtualenv site-packages path to the sys.path
sys.path.append('/home/ubuntu/virtualenvs/30env/lib/python3.6/site-packages')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thirtyworks.settings')

application = get_wsgi_application()