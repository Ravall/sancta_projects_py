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


#TINYMCE_DEFAULT_CONFIG = {
#    'content_css': "/static/css/tinymce_content.css",
#    'plugins': "table,spellchecker,paste,searchreplace,advhr,insertdatetime",
#    'theme': "advanced",
#    'cleanup_on_startup': True,
#    'custom_undo_redo_levels': 10,
#    'style_formats': [
#        {'title': 'Тест 1', 'block': 'p', 'classes': 'test1'},
#        {'title': 'Тест 2', 'inline': 'span', 'classes': 'test2'},
#    ],
#    'verify_html': False,
#    'height': '800px',
#    "theme_advanced_buttons1": "addArticle,addEvent,bold," +
#    "italic,underline,strikethrough,|,justifyleft," +
#    "justifycenter,justifyright,justifyfull,|,styleselect," +
#    "formatselect,fontselect,fontsizeselect,|,spellchecker",
#    "theme_advanced_buttons2": "cut,copy,paste,|,search,replace," +
#    "|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo," +
#    "|,link,unlink,image,cleanup,code,|,forecolor,backcolor,|," +
#    "insertfile,insertimage",
#    "theme_advanced_buttons3": "tablecontrols,|,hr,removeformat," +
#    "visualaid,|,sub,sup,|,charmap,emotions,iespell,media,advhr",
#    'language': 'ru',
#    'setup': """function(ed) {
#        // Add a custom button
#        ed.addButton('addArticle', {
#            title : 'add article',
#            image : '/media/upload/article_icon.png',
#            onclick : function() {
#                ed.focus();
#                cnt = ed.selection.getContent()
#                ed.selection.setContent(
#                    '<sacticle name="" id="">'+cnt+'</sacticle>'
#                );
#            }
#        });
#        ed.addButton('addEvent', {
#            title : 'add event',
#            image : '/media/upload/calendar_new.png',
#            onclick : function() {
#                ed.focus();
#                cnt = ed.selection.getContent()
#                ed.selection.setContent(
#                    '<sevent name="" id="">'+cnt+'</sevent>'
#                );
#            }
#        });
#   }"""
#
#
#}
#TINYMCE_SPELLCHECKER = True
#TINYMCE_FILEBROWSER = True
#TINYMCE_COMPRESSOR = True

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
