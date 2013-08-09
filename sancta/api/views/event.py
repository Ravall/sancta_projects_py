# -*- coding: utf-8 -*-
# pylint: disable=W0613, W0622
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from mf_calendar.models import MfCalendarEvent
from api.models import prepare_event, prepare_events
from api.decorator import responsed, cached_result


@api_view(['GET'])
@responsed
@cached_result('event-api')
def get_event(request, event_id, format):
    try:
        params = {
            'status': 'active',
            'id' if event_id.isdigit() else 'url': event_id
        }
        event = MfCalendarEvent.objects.get(**params)
    except ObjectDoesNotExist:
        return False
    return prepare_event(event)


@api_view(['GET'])
@responsed
@cached_result('articletag-api')
def get_events_by_tag(request, event_tag, format):
    events = MfCalendarEvent.objects.filter(
        tags__name__in=[event_tag],
        status='active'
    )
    if not events:
        return False
    return prepare_events(events)


@api_view(['GET'])
@responsed
@cached_result('eventall-api')
def get_all_events(request, format):
    events = MfCalendarEvent.objects.filter(status='active')
    if not events:
        return False
    return prepare_events(events)
