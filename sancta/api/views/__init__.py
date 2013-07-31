# -*- coding: utf-8 -*-
# pylint: disable=W0613, W0622
from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from mf_calendar.models import MfCalendarNet, MfCalendarEvent
from mf_system.models import MfSystemArticle
from api.models import prepare_event, prepare_events, \
    prepare_article, prepare_articles
from smart_date.date import is_date_correct


@api_view(['GET'])
def get_articles(request, article_id, format):
    """
    возвращает информацию о статьях
    """
    try:
        params = {
            'status': 'active',
            'id' if article_id.isdigit() else 'url': article_id
        }
        article = MfSystemArticle.objects.get(**params)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(prepare_article(article, add_related=True))


@api_view(['GET'])
def get_articles_by_tag(request, article_tag, format):
    articles = MfSystemArticle.objects.filter(
        tags__name__in=[article_tag],
        status='active'
    )
    if not articles:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(prepare_articles(articles))


class Calendar(APIView):
    @staticmethod
    def prepare_day_data(events, day):
        day_events = []
        for event in events:
            day_events.append(prepare_event(
                event,
                show_text=True,
                show_icons=True,
                show_articles=True
            ))
        return Response({
            'date': day,
            'events': day_events,
        })

    def get(self, request, day, format):
        if not is_date_correct(*day.split('-')[::-1]):
            return Response(status=status.HTTP_404_NOT_FOUND)
        days = MfCalendarNet.objects.filter(full_date=day)
        event_ids = [
            calendar_day.event_id for calendar_day in days
            if calendar_day.event_id > 0
        ]
        events = MfCalendarEvent.objects.filter(
            pk__in=event_ids, status='active'
        )
        return self.prepare_day_data(events, day)


@api_view(['GET'])
def get_event(request, event_id, format):
    try:
        params = {
            'status': 'active',
            'id' if event_id.isdigit() else 'url': event_id
        }
        event = MfCalendarEvent.objects.get(**params)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(prepare_event(event))


@api_view(['GET'])
def get_events_by_tag(request, event_tag, format):
    events = MfCalendarEvent.objects.filter(
        tags__name__in=[event_tag],
        status='active'
    )
    if not events:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(prepare_events(events))


@api_view(['GET'])
def get_all_events(request, format):
    events = MfCalendarEvent.objects.filter(status='active')
    if not events:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(prepare_events(events))


@api_view(['GET'])
def get_example(request, format):
    resource_urls = [
        reverse(
            'event-api', kwargs={'event_id': 29, 'format': 'json'},
            request=request
        ),
        reverse(
            'eventall-api', kwargs={'format': 'json'},
            request=request
        ),
        reverse(
            'article-api', kwargs={'article_id': 231, 'format': 'json'},
            request=request
        ),
        reverse(
            'articletag-api', kwargs={'article_tag': 'post', 'format': 'json'},
            request=request
        ),
        reverse(
            'calendar-api', kwargs={'day': '2012-10-14', 'format': 'json'},
            request=request
        )
    ]
    return Response({"example": resource_urls})
