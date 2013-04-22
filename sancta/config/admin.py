# -*- coding: utf-8 -*-
# pylint: disable=W0403,W0614,W0611,W0401
from _admin import *
from databases import DATABASES
TEMPLATE_DEBUG = True

ROOT_URLCONF = 'sancta.urls'
WSGI_APPLICATION = 'sancta.wsgi.application'

# переопределим на бою урл, чтобы смотрел на сервер изображений
FILEBROWSER_MEDIA_URL = 'http://img.sancta.ru/'

ALLOWED_HOSTS = 'admin2.sancta.ru'