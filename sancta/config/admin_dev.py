# -*- coding: utf-8 -*-
# pylint: disable=W0403,W0614,W0611,W0401
from _admin import *
LOGGING['loggers']['sancta_log']['level'] = 'INFO'
from databases_dev import DATABASES
TEMPLATE_DEBUG = True
ROOT_URLCONF = 'sancta.urls'
WSGI_APPLICATION = 'sancta.wsgi.application'
MEDIA_HOST = 'http://127.0.0.1:8000/media/'
# django debug toolbar
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
INSTALLED_APPS += ('debug_toolbar', 'api')

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.cache.CacheDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)
INTERNAL_IPS = ('127.0.0.1',)
NGINX_CACHE = '/tmp'

FOREIGN_SITE_ID = 3
