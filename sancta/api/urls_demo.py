from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views_demo

# pylint: disable=C0103
urlpatterns = patterns('api.views_demo',
    url(r'^$', views_demo.index, name='index'),
    url(r'^smartdate/$', views_demo.smartdate, name="smartdate"),
    url(r'^docs/$', views_demo.docs, name="docs"),
    url(r'^docs/calendar$', views_demo.docs_calendar, name="docs_calendar"),
    url(r'^docs/articles$', views_demo.docs_articles, name="docs_articles"),
    url(r'^requires/$', views_demo.requires, name='requires'),
    url(r'^contacts/$', views_demo.contacts, name='contacts')
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
