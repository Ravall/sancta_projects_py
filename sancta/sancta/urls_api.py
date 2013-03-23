from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^', include('api.urls_demo')),
    url(r'^api', include('api.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
