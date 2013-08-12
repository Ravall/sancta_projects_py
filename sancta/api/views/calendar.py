# -*- coding: utf-8 -*-
# pylint: disable=W0613, W0622
from rest_framework.decorators import api_view
from mf_calendar.models import MfCalendarNet, MfCalendarEvent
from api.decorator import responsed, cached_result
from smart_date.date import is_date_correct
from api.models import prepare_event


def resp_day(events, day):
    day_events = []
    for event in events:
        day_events.append(
            prepare_event(
                event,
                show_text=True,
                show_icons=True,
                show_articles=True
            )
        )
    return dict(
        date=day,
        events=day_events,
    )


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
    return resp_day(events, day)
