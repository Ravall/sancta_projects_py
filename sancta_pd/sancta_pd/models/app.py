# -*- coding: utf-8 -*-
import pyramid
'''
дополнительные модели, применимые ко всему приложению
'''


def get_config(key):
    '''

    '''
    registry = pyramid.threadlocal.get_current_registry()
    print registry.settings
    return registry.settings[key]