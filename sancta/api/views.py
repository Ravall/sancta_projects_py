# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from djangorestframework.views import View
from djangorestframework.reverse import reverse
from djangorestframework.response import Response
from djangorestframework import status
from mf_calendar import models as calendar_model
from tools import api


class CalendarView(View):
    '''
    Выводит информацию о дне календаря.
    '''
    def prepare_day_data(self, days):
        icons = calendar_model.MfCalendarIcon.get_by_events(
            [{'id': day.event_id} for day in days]
        )
        # выделим "уникальные" иконы
        # т.е от каждого события по одной иконе
        tmp = set()
        unicicons = set()
        for icon in icons:
            if not icon.event_id in tmp:
                unicicons.add(icon)
                tmp.add(icon.event_id)
        return {
            # все иконы
            'icons': api.prepare_icons(icons),
            # по одной иконе для event
            'icons_unic': api.prepare_icons(unicicons),
        }

    '''
    api к календарю
    '''
    def get(self, request, day):
        try:
            day = calendar_model.MfCalendarNet.objects.filter(full_date=day)
        except ObjectDoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)
        return self.prepare_day_data(day)


class EventView(View):
    '''
    выдает информацию о событию
    '''
    def get(self, request, num):
        try:
            event = calendar_model.MfCalendarEvent.objects.get(pk=num)
        except ObjectDoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)
        return api.prepare_event(event)


class ApiView(View):
    """
    Примеры api
    """
    def get(self, request):
        """
        Handle GET requests, returning a list of URLs pointing to 3 other views.
        """
        resource_urls = [
            reverse('event-api', kwargs={'num': 29}, request=request),
            reverse('calendar-api', kwargs={'day': '2012-10-14'}, request=request)
        ]
        return {"example": resource_urls}
