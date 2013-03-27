from django.conf.urls.defaults import patterns, url

# pylint: disable=C0103
urlpatterns = patterns('orthcalendar.views',
#    url(
#        r'^$', 'get_example', name='api-resources',
#    ),
    url(r'^article/(?P<article>[0-9a-z_]+)$', 'get_article', name='art'),
)
