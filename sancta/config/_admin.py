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
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
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
    'tinymce',
    'file_picker',
    'file_picker.uploads', # file and image Django app
    #'file_picker.wymeditor', # optional WYMeditor plugin
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

ADMIN_TOOLS_INDEX_DASHBOARD = 'sancta.dashboard.CustomIndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'sancta.dashboard.CustomAppIndexDashboard'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.JSONPRenderer',
        'rest_framework.renderers.XMLRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )
}
REST_SUFFIX_ALLOWED = ['json', 'xml', 'api']


#TINYMCE_JS_URL = 'http://debug.example.org/tiny_mce/tiny_mce_src.js'
TINYMCE_DEFAULT_CONFIG = {
    'content_css' : "/static/css/tinymce_content.css",
    'plugins': "table,spellchecker,paste,searchreplace",
    'theme': "advanced",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
    #'font_size_style_values': "xx-large",
    #'theme_advanced_font_sizes': "20px",
    'style_formats' : [
        {'title' : 'Тест 1', 'block' : 'p', 'classes' : 'test1' },
        {'title' : 'Тест 2', 'inline' : 'span', 'classes' : 'test2'},
    ],
}
TINYMCE_SPELLCHECKER = True
TINYMCE_FILEBROWSER = True
#TINYMCE_COMPRESSOR = True

DIRECTORY = 'uploads/'

URL_FILEBROWSER_MEDIA = STATIC_URL + "filebrowser/"
PATH_FILEBROWSER_MEDIA = os.path.join(STATIC_ROOT, 'filebrowser/')

URL_TINYMCE = ADMIN_MEDIA_PREFIX + "tinymce/jscripts/tiny_mce/"
PATH_TINYMCE = ADMIN_MEDIA_PREFIX + "tinymce/jscripts/tiny_mce/"