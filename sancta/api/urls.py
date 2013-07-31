from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import patterns, url
from django.conf import settings
from api.views import Calendar

# pylint: disable=C0103
urlpatterns = patterns(
    'api.views',
    url(r'^$', 'get_example', name='api-resources'),
    url(
        r'^/event/tag/(?P<event_tag>[0-9a-z_]+)$', 'get_events_by_tag',
        name='eventtag-api'
    ),
    url(r'^/event/all$', 'get_all_events', name='eventall-api'),
    url(
        r'^/event/(?P<event_id>[0-9a-z_]+)$', 'get_event',
        name='event-api'
    ),
    url(
        r'^/article/(?P<article_id>[0-9a-z_]+)$', 'get_articles',
        name='article-api'
    ),
    url(
        r'^/article/tag/(?P<article_tag>[0-9a-z_]+)$', 'get_articles_by_tag',
        name='articletag-api'
    ),
    url(
        r'^/calendar/(?P<day>[0-9]{4}-[0-9]{2}-[0-9]{2})$',
        Calendar.as_view(), name='calendar-api'
    )
)

urlpatterns = format_suffix_patterns(
    urlpatterns, suffix_required=True,
    allowed=settings.REST_SUFFIX_ALLOWED
)
