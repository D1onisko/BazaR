# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('src.apps.catalogue.views',

    url(r'^$', 'index', name='index'),
    url(r'^category/(?P<pk>[^/]+)/$', 'category', name='category'),
    url(r'^product/(?P<pk>[^/]+)/$', 'product_detail', name='product_detail'),


)