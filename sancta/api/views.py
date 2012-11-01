# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist

from djangorestframework.views import View
from djangorestframework.reverse import reverse
from djangorestframework.response import Response
from djangorestframework import status



from mf_calendar import models as calendar_model

class CalendarView(View):
	def prepare_day_data(self, event):
		pass

	'''
	api к календарю
	'''
	def get(self, request, num):
		try:
			pass
		except ObjectDoesNotExist:
			return Response(status.HTTP_404_NOT_FOUND)
		return self.prepare_day_data(event[0])


class EventView(View):

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
		    'icons': [{
		    	'id': icon.id,
		    	'text': {
		    		'id': icon.id,
		    		'title': icon.title,
		    		'content': icon.content,
		    	},
		    	'image': icon.image,
		    	'urls': {
		    	    'origin': 'http://img.sancta.ru/origin/%s' % icon.image,
		    	    '150x200': 'http://img.sancta.ru/crop/150x200/%s' % icon.image
		    	}
		     } for icon in event.get_icons()],
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




