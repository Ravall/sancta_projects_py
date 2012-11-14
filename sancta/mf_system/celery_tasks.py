# -*- coding: utf-8 -*-
import celery
import os
from md5 import md5


def remove_cach_file_by_url(url):
    file_name = md5(url).hexdigest()
    file_path = os.path.abspath(os.path.join(NGINX_CACHE, file_name))
    os.remove(file_path)


def event_info_update(id):
    remove_cach_file_by_url(reverse('event-api', kwargs={'num': id}))


def calendar_update(date):
    remove_cach_file_by_url(reverse('calendar-api', kwargs={'day': date}))


def event_calendar_update(id):
    #для каждой даты по умной фунции вызовем метод очищения
    event = MfCalendarEvent.objects.get(pk=id)
    # пройдемся по "быстрым годам"
    for year in range(SMART_FUNCTION_YEAR_BEGIN, SMART_FUNCTION_YEAR_END):
        # для каждого года получим дату
        for date in event.function.getDates(year):
            # подчистим для каждой даты кэш
            calendar_update(date)


@celery.task(name='event:update')
def event_update(id):
    event_info_update(id)
    event_calendar_update(id)
