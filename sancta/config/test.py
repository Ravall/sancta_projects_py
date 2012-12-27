# -*- coding: utf-8 -*-
# pylint: disable=W0403,W0611
import os
from common import SECRET_KEY, SITE_ID, _PATH
ROOT_URLCONF = 'sancta.urls'
from databases_test import DATABASES
# приложения, которые нужно тестировать
IS_TESTING = 1
MEDIA_HOST = 'http://testurl.dev/'
FIXTURE_DIRS = os.path.join(_PATH, '/sancta/fixtures/'),
# для тестов достаточно 2-х лет :-)
SMART_FUNCTION_YEAR_BEGIN = 2010
SMART_FUNCTION_YEAR_END = 2011
INSTALLED_APPS = (
    'django.contrib.sites',
    'south',
    'sancta',
    'django.contrib.contenttypes',
    'taggit',
    'mf_system',
    'api',
    'tools',
)
REST_SUFFIX_ALLOWED = ['json', 'xml']
