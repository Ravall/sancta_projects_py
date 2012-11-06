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
		return {
			'icons': api.prepare_icons(icons),
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

	def prepare_event_data(self, event):
		'''
		контролируем выводиме данные. ничего лишнего, только то, что нужно
		'''
		return {
		    'id': event.id,
		    'text': {
		        'title': event.title,
		        'annonce': event.annonce,
		        'content': event.content,
		    },
		    'image': event.image,
		    'icons': api.prepare_icons(event.get_icons()),
		}

	'''
	api к event
	'''
	def get(self, request, num):
		try:
			event = calendar_model.MfCalendarEvent.objects.filter(pk=num)
		except ObjectDoesNotExist:
			return Response(status.HTTP_404_NOT_FOUND)
		return self.prepare_event_data(event[0])


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




