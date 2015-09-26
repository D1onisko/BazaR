# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from src.apps.search.views import ProductSearchView


urlpatterns = patterns('src.apps.search.views',

    url(r'^search/$', ProductSearchView.as_view(), name='haystack_search'),

)
