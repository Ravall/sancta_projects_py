from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from api.views import demo

# pylint: disable=C0103
urlpatterns = patterns(
    'api.demo',
    url(r'^$', demo.index, name='index'),
    url(r'^smartdate/$', demo.smartdate, name="smartdate"),
    url(r'^docs/$', demo.docs, name="docs"),
    url(r'^docs/calendar$', demo.docs_calendar, name="docs_calendar"),
    url(r'^docs/articles$', demo.docs_articles, name="docs_articles"),
    url(r'^requires/$', demo.requires, name='requires'),
    url(r'^contacts/$', demo.contacts, name='contacts')
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
