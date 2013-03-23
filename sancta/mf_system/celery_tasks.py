# -*- coding: utf-8 -*-
import celery
import os
import logging
from md5 import md5
from django.conf import settings
from smart_date.smartfunction import smart_function
from smart_date.date import yyyy_mm_dd
from rest_framework.reverse import reverse


@celery.task
def cc_event_info(event_id):
    '''
    удалим nginx кэш информации о событии
    '''
    remove_cach_file_by_url(
        reverse('event-api', kwargs={'num': event_id})
    )


@celery.task
def cc_smart_function(function):
    '''
    удалим кэш для дат фунции
    '''
    for year in range(settings.SMART_FUNCTION_YEAR_BEGIN,
                      settings.SMART_FUNCTION_YEAR_END):
        # для каждого года получим дату
        for date in smart_function(function, year):
            # подчистим для каждой даты кэш
            remove_cach_file_by_url(
                reverse('calendar-api', kwargs={'day': yyyy_mm_dd(date)})
            )


def remove_cach_file_by_url(url):
    url += '?format=json'
    logger = logging.getLogger('sancta_log')
    logger.info('чистим кэш по урлу {0}'.format(url))
    file_name = md5(url).hexdigest()
    file_path = os.path.abspath(os.path.join(settings.NGINX_CACHE, file_name))
    try:
        os.remove(file_path)
    except OSError:
        pass
