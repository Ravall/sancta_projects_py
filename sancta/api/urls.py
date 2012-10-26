from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
      url(r'^icons/(?P<event_id>\d+)/','api.views.get_icons_by_event_id')
)
