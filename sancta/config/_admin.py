# -*- coding: utf-8 -*-
# pylint: disable=W0403,W0614,W0611,W0401
from common import *
# celery
import djcelery
djcelery.setup_loader()
#BROKER_URL = 'amqp://'
BROKER_URL = 'django://'
BROKER_BACKEND = "djkombu.transport.DatabaseTransport"
#BROKER_BACKEND = "amqp"
CELERY_IMPORTS = "hell.sabnac", "hell.azazel", "hell.anubis"

INSTALLED_APPS += (
    'gunicorn',
    'grappelli.dashboard',
    'grappelli',
    'filebrowser',
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'django.contrib.messages',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.messages',
    'django.contrib.admin',
    'sancta',
    'mf_system',
    'mf_calendar',
    'mf_admin',
    'api',
    'tools',
    'djcelery',
    'kombu.transport.django',
    'south',
    'taggit',
    'ckeditor',
    'taggit_autocomplete_modified'
)

FILEBROWSER_DIRECTORY = 'origin'

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',

    # django 1.2 only
    'django.contrib.messages.context_processors.messages',

    # required by django-admin-tools
    'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES += (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

# года, которые интересны для быстрой работы
# по ним оперативно чистится кэш, оперативно выбираются события
SMART_FUNCTION_YEAR_BEGIN = 1900
SMART_FUNCTION_YEAR_END = 2100

GRAPPELLI_INDEX_DASHBOARD = 'sancta.dashboard_grappelli.CustomIndexDashboard'


REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.JSONPRenderer',
        'rest_framework.renderers.XMLRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )
}
REST_SUFFIX_ALLOWED = ['json', 'xml', 'api']

# Filebrowser
DIRECTORY = ''
FILEBROWSER_DEBUG = True

# Test for or create a dashboard file
FILEBROWSER_DIRECTORY = 'images/'
FILEBROWSER_MAX_UPLOAD_SIZE = 2097152
FILEBROWSER_SAVE_FULL_URL = False
FILEBROWSER_VERSIONS_BASEDIR = "versions"
FILEBROWSER_ADMIN_VERSIONS = {
    'admin_thumbnail': {
        'verbose_name': 'Admin Thumbnail',
        'width': 60,
        'height': 60,
        'opts': 'crop'
    },
}

# Grappelli
GRAPPELLI_ADMIN_TITLE = 'АдмЫнка.'
GRAPPELLI_ADMIN_URL = 'admin/'


#CK
CKEDITOR_UPLOAD_PATH = os.path.join(UPLOAD_MEDIA_ROOT, 'fck')
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Full',
        'height': 400,
        'forcePasteAsPlainText': True,
    },
}

API_CACHE_TIME = 60
