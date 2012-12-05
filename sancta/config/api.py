# -*- coding: utf-8 -*-
from common import *
from databases import DATABASES
TEMPLATE_DEBUG = False
ROOT_URLCONF = 'sancta.urls_api'
# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'sancta.wsgi_api.application'
MEDIA_HOST = 'http://img.sancta.ru/'
NGINX_CACHE = '/home/var/cache'
