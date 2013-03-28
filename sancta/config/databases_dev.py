# -*- coding: utf-8 -*-
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sancta_dj',
        'USER': 'sancta_user',
        'PASSWORD': 'sancta_user_password',
        'HOST': '127.0.0.1',
        'PORT': '',
    },
    'sancta_db' : {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mindfly',
        'USER': 'sancta_user',
        'PASSWORD': 'sancta_user_password',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}