# -*- coding: utf-8 -*-
# pylint: disable=W0403,W0614,W0611,W0401
from _api import *
from databases import DATABASES
from hashlib import md5

TEMPLATE_DEBUG = False
# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'sancta.wsgi_api.application'
MEDIA_HOST = 'http://img.sancta.ru/'
ALLOWED_HOSTS = ['api.sancta.ru', 'api.sancta.local']
FOREIGN_SITE_ID = 3
