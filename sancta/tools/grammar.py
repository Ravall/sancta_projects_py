# -*- coding: utf-8 -*-
# ругается что модуль trans не используется - ложь
# pylint: disable=W0611  
import trans

def translite(string):
    '''
    транслитерация. подходит для seo
    '''
    def eu8(string):
        return string.encode('utf-8')

    return eu8(unicode(string.replace(' ', '_')).encode('trans').lower())
