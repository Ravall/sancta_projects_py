from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings



admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sancta.views.home', name='home'),
    # url(r'^sancta/', include('sancta.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^api/',include('api.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^restframework/', include('djangorestframework.urls', namespace='djangorestframework')),
    url(r'^', include('orthcalendar.urls')),
)