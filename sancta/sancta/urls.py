from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from orthcalendar.views import generate_sitemap_view


admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sancta.views.home', name='home'),
    # url(r'^sancta/', include('sancta.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'act/sitemap', generate_sitemap_view),
    url(r'^api/',include('api.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^restframework/', include('djangorestframework.urls', namespace='djangorestframework')),
    url(r'^admin_tools/', include('admin_tools.urls'))
)


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        urlpatterns += staticfiles_urlpatterns()