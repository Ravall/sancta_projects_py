# pylint: disable=W0403,W0614,W0611,W0401
from common import *
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

ROOT_URLCONF = 'sancta.urls_api'
TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

MIDDLEWARE_CLASSES += (
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware'
)

INSTALLED_APPS += (
    'django.contrib.messages',
    'template_bootstrap',
    'api'
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.contrib.messages.context_processors.messages',
)

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.JSONPRenderer',
        'rest_framework.renderers.XMLRenderer',
    )
}
REST_SUFFIX_ALLOWED = ['json', 'xml']

SITE_HASH = {
    '8euz2cpm': 1,
    'x3qb5hh6': 2
}
GRACEFUL_STATEDIR = '/home/var/run/api/'