# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from src.apps.search.views import JohnSearchView


urlpatterns = patterns('src.apps.search.views',

    url(r'^search/$', JohnSearchView.as_view(), name='haystack_search'),

)
