from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

urlpatterns = patterns('',
    url(r'^api/',include('api.urls')),
    url(r'^restframework/', include('djangorestframework.urls', namespace='djangorestframework')),
)




