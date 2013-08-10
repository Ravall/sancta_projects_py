# -*- coding: utf-8 -*-
# pylint: disable=W0613, W0622
from rest_framework.decorators import api_view
from mf_calendar.models import MfCalendarNet, MfCalendarEvent
from api.models import prepare_day
from api.decorator import responsed, cached_result
from smart_date.date import is_date_correct


@api_view(['GET'])
@responsed
@cached_result('calendar-api')
def get_day(request, day, format):
    if not is_date_correct(*day.split('-')[::-1]):
        return False
    days = MfCalendarNet.objects.filter(full_date=day)
    event_ids = [
        calendar_day.event_id for calendar_day in days
        if calendar_day.event_id > 0
    ]
    events = MfCalendarEvent.objects.filter(
        pk__in=event_ids, status='active'
    )
    return prepare_day(events, day)
