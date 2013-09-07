# -*- coding: utf-8 -*-
# pylint: disable=W0403,W0614,W0611
import os
import platform

_PATH = os.path.abspath(os.path.dirname(__file__) + '/../')
# DEBUG должен находится тут
DEBUG = platform.node() != 'sancta'
SERVER_EMAIL = 'valery.ravall@gmail.com'
ADMINS = (
    ('Ravall', SERVER_EMAIL),
)
MANAGERS = ADMINS


DATABASE_ROUTERS = [
    'sancta.db_router.Sancta_Router',
]
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Moscow'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru-RU'

SITE_ID = 1
# сайт изучения иностранного языка
FOREIGN_SITE_ID = 0

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"


# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.abspath(os.path.join(_PATH, '../', 'files', 'media'))
ORIGIN_MEDIA_ROOT = os.path.join(MEDIA_ROOT, 'origin')
# в эту папку будет все загружено из вне.
UPLOAD_MEDIA_ROOT = os.path.join(MEDIA_ROOT, 'upload')
#DIRECTORY = '/upload'
# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"

STATIC_ROOT = os.path.abspath(
    os.path.join(_PATH, '../', 'files', 'collected_static')
)

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
SITEMAP = os.path.abspath(os.path.join(MEDIA_ROOT, 'sitemap.xml'))
# Additional locations of static files

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',

    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '54%cgx5&amp;s0fs+no3!#)hbvou%u0p2g&amp;)b-+ct3jj$31-^e#z2h'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    os.path.join(_PATH, '../', 'templates')
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
)


TEMPLATE_CONTEXT_PROCESSORS = (
    # default template context processors
    'django.core.context_processors.media',
    'django.core.context_processors.static',
)

INSTALLED_APPS = (
    'gunicorn',
    'django.contrib.staticfiles',
    'sancta',
    'rest_framework',
    'raven.contrib.django.raven_compat'
)


# Также в settings.py можно добавить словарь GRACEFUL_OPTIONS,
# указав в нём дополнительные опции для команды «./manage.py runfcgi».
# GRACEFUL_OPTIONS

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),
    'PAGINATE_BY': 100,
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': "%(levelname)s %(asctime)s " +
            "%(module)s %(process)d %(thread)d %(message)s"
        },
        'simple': {
            'format': '[%(levelname)s|%(asctime)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'log_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.abspath(
                os.path.join(_PATH, '../', 'files', 'logs', 'sancta.log')
            ),
            'formatter': 'simple'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'sancta_log': {
            'handlers': ['log_file'],
            'level': 'ERROR',
            'propagate': True,
        }
    }
}

IS_TESTING = 0

API_CACHE = '/home/var/cache'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/home/var/cache_'
    },
    'api': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': API_CACHE,
    }
}

if DEBUG:
    RAVEN_CONFIG = {
        'dsn': 'http://d8269d2266544e8cba773709c27cfcd8:a6aa0e1c95d444729b810d2ee8648420@0.0.0.0:9000/2',
    }
