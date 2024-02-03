"""
WSGI config for sakura project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from os import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sakura.settings')

sys.path.append('/var/www')
sys.path.append('/var/www/sakura')


application = get_wsgi_application()
