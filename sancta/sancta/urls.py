from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from orthcalendar.views import generate_sitemap_view
from filebrowser.sites import site


admin.autodiscover()

urlpatterns = patterns('',
    url(r'act/sitemap', generate_sitemap_view),
    url(r'^api', include('api.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin_tools/', include('admin_tools.urls')),
    #url(r'^tinymce/', include('tinymce.urls')),

    url(r'^grappelli/', include('grappelli.urls')),
    #url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^ckeditor/', include('ckeditor.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
