from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.defaults import patterns, url
from api.views import ApiView, EventView, CalendarView


urlpatterns = patterns('',
    url(
    	r'^$', 
    	ApiView.as_view(), 
    	name='api-resources'
    ),
    url(
    	r'^event/(?P<id_or_name>[0-9a-z_]+)/$', 
    	EventView.as_view(), 
    	name='event-api'
    ),
    url(
    	r'^calendar/(?P<day>[0-9]{4}-[0-9]{2}-[0-9]{2})/$', 
    	CalendarView.as_view(), 
    	name='calendar-api'
    )
)