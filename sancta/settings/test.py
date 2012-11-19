# -*- coding: utf-8 -*-
from sancta.settings_common import SECRET_KEY
from databases_test import DATABASES
# приложения, которые нужно тестировать
INSTALLED_APPS = (
    'mf_system',
    'api',
    'tools',
)
