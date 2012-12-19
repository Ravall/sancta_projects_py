# -*- coding: utf-8 -*-
# pylint: disable=E1102

'''
САБНАК - демон, ответственный за гниение трупов.
------------
удаляет старый кэш
    cc_event_info       кэш информации о событии
    cc_smart_function   кэш для дат фунции
'''

import celery
import os
import logging
from md5 import md5
from tools.date import yyyy_mm_dd
from django.conf import settings
from tools.smartfunction import smart_function
from djangorestframework.reverse import reverse
from mf_calendar import models as calendar_model


@celery.task(name='чистить кэш по event_id')
def cc_event_info(event_id):
    '''
    удалим nginx кэш информации о событии
    '''
    _remove_cach_file_by_url(
        reverse('event-api', kwargs={'id_or_name': event_id})
    )
    event = calendar_model.MfCalendarEvent.objects.get(pk=event_id)
    _remove_cach_file_by_url(
        reverse('event-api', kwargs={'id_or_name': event.url})
    )


@celery.task(name='чистить кэш по датам')
def cc_smart_function(function):
    '''
    удалим кэш для дат фунции
    '''
    for year in range(settings.SMART_FUNCTION_YEAR_BEGIN,
                      settings.SMART_FUNCTION_YEAR_END):
        # для каждого года получим дату
        for date in smart_function(function, year):
            # подчистим для каждой даты кэш
            _remove_cach_file_by_url(
                reverse('calendar-api', kwargs={'day': yyyy_mm_dd(date)})
            )


def _remove_cach_file_by_url(url):
    url += '?format=json'
    logger = logging.getLogger('sancta_log')
    logger.info('clear cache by url {0}'.format(url))
    file_name = md5(url).hexdigest()
    file_path = os.path.abspath(os.path.join(settings.NGINX_CACHE, file_name))
    try:
        os.remove(file_path)
    except OSError:
        pass
