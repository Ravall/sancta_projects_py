from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^api/',include('api.urls')),
    url(r'^restframework/', include('djangorestframework.urls', namespace='djangorestframework')),
)




