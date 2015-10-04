from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^search/', include('haystack.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    url(r'^', include('src.apps.catalogue.urls', namespace='catalogue')),
    url(r'^', include('src.apps.search.urls', namespace='search', )),
    url(r'^', include('src.apps.dashboard.urls', namespace='dashboard')),

)
