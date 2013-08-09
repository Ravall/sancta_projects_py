# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.cache import get_cache
from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse


def responsed(func):
    '''
    оборачиваем в респонс
    '''
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if not result:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(result)
    return wrapper


def cached_result(route_name):
    """
    кэшированный результат.
    не обернутый в респонс
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            if settings.IS_TESTING:
                # если режим тестирования кэшировать не нужно
                return func(*args, **kwargs)
            cache = get_cache('api')
            cache_key = reverse(route_name, kwargs=kwargs)
            result = cache.get(cache_key)
            if result:
                # если кэш удалось получить - возвращаем его
                return result
            result = func(*args, **kwargs)
            if result:
                # если удалось получить значение метода - сохраняем его в кэш
                cache.set(cache_key, result, settings.API_CACHE_TIME)
            return result
        return wrapper
    return decorator
