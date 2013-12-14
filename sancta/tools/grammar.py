# -*- coding: utf-8 -*-
# ругается что модуль trans не используется - ложь
# pylint: disable=W0611
import trans
import re


def translite(string):
    '''
    транслитерация. подходит для seo
    '''
    def eu8(string):
        return string.encode('utf-8')
    if string[-1] == '.':
        string = string[0:-1]
    return re.sub(
        '[^0-9a-z_]', '_',
        eu8(unicode(string.lower()).encode('trans'))
    )


