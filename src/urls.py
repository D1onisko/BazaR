from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^search/', include('haystack.urls')),

    url(r'^', include('src.apps.catalogue.urls', namespace='catalogue')),
    url(r'^', include('src.apps.search.urls', namespace='search', )),
    url(r'^', include('src.apps.dashboard.urls', namespace='dashboard')),

)
