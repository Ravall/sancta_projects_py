# -*- coding: utf-8 -*-
"""
clear cache
тут собраны методы для правильной очистки кэша
"""
import os
import logging
from hashlib import md5
from django.conf import settings
from django.contrib.sites.models import Site
from rest_framework.reverse import reverse
from smart_date.smartfunction import smart_function
from smart_date.date import yyyy_mm_dd


def by_event_id(event_id):
    _remove_cach_file_by_route('event-api', {'event_id': event_id})


def by_article_id(article_id, site_id):
    site = Site.objects.get(pk=site_id)
    _remove_cach_file_by_route(
        'article-api', {
            'article_id': article_id,
            'site_name': site.name
        }
    )


def by_article_tag(tag, site_id):
    site = Site.objects.get(pk=site_id)
    _remove_cach_file_by_route(
        'articletag-api', {
            'article_tag': tag,
            'site_name': site.name
        }
    )


def by_article_url(url, site_id):
    site = Site.objects.get(pk=site_id)
    _remove_cach_file_by_route(
        'article-api', {
            'article_id': url,
            'site_name': site.name
        }
    )


def by_event_url(url):
    _remove_cach_file_by_route('event-api', {'event_id': url})


def by_smart_function(function):
    '''
    удалим кэш для дат фунции
    '''
    for year in xrange(
        settings.SMART_FUNCTION_YEAR_BEGIN,
        settings.SMART_FUNCTION_YEAR_END + 1
    ):
        # для каждого года получим дату
        for date in smart_function(function, year):
            # подчистим для каждой даты кэш
            _remove_cach_file_by_route(
                'calendar-api', {'day': yyyy_mm_dd(date)}
            )


def _remove_cach_file_by_route(route_name, kwargs):
    for frm in settings.REST_SUFFIX_ALLOWED:
        kwargs['format'] = frm
        _remove_cach_file_by_url(
            reverse(route_name, kwargs=kwargs)
        )


def _remove_cach_file_by_url(url):
    # проходимся по суффиксам
    logger = logging.getLogger('sancta_log')
    logger.info('clear cache by url {0}'.format(url))
    file_name = md5(url).hexdigest()
    file_path = os.path.abspath(os.path.join(settings.NGINX_CACHE, file_name))
    try:
        os.remove(file_path)
    except OSError:
        pass
