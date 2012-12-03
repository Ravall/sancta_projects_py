# -*- coding: utf-8 -*-
# Django settings for sancta project.
import os
import platform
# celery
import djcelery

_PATH = os.path.abspath(os.path.dirname(__file__) + '/../')
# DEBUG должен находится тут
DEBUG = platform.node() != 'sancta'
ADMINS = (
    ('Ravall', 'valery.ravall@gmail.com'),
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

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

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
# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"

STATIC_ROOT = os.path.abspath(os.path.join(_PATH, '../', 'files', 'collected_static'))

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

# Additional locations of static files

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '54%cgx5&amp;s0fs+no3!#)hbvou%u0p2g&amp;)b-+ct3jj$31-^e#z2h'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)


TEMPLATE_DIRS = (
    os.path.join(_PATH, '../', 'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'mf_system',
    'api',
    'djangorestframework',
    'tools',
    'djcelery',
    'kombu.transport.django',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
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
        'sancta_log' : {
            'handlers': ['log_file'],
            'level': 'ERROR',
            'propagate': True,
        }
    }
}

djcelery.setup_loader()
#BROKER_URL = 'amqp://'
BROKER_URL = 'django://'
BROKER_BACKEND = "djkombu.transport.DatabaseTransport"
#BROKER_BACKEND = "amqp"
CELERY_IMPORTS = ("mf_system.celery_tasks",)

# года, которые интересны для быстрой работы
# по ним оперативно чистится кэш, оперативно выбираются события
SMART_FUNCTION_YEAR_BEGIN = 1950
SMART_FUNCTION_YEAR_END = 2050
NGINX_CACHE = ''
