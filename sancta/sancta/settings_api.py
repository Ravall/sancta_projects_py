# -*- coding: utf-8 -*-
from settings import *
from databases import DATABASES
TEMPLATE_DEBUG = False
ROOT_URLCONF = 'sancta.urls_api'
# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'sancta.wsgi_api.application'