# -*- coding: utf-8 -*-
import trans

def translite(string):
    '''
    транслитерация. подходит для seo
    '''
    def u8(string):
        return unicode(string)

    def eu8(string):
        return string.encode('utf-8')

    return eu8(u8(string.replace(' ', '_')).encode('trans').lower())