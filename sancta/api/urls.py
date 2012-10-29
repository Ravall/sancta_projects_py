from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.defaults import patterns, url
from api.views import ApiView, EventView

urlpatterns = patterns('',
    url(r'^$',                 ApiView.as_view(), name='api-resources'),
    url(r'^event/(?P<num>[0-9]+)/icon/$', EventView.as_view(), name='event-api')
)