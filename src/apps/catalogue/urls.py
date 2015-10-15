# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from src.apps.catalogue.views import IndexView, DetailProductView, ProductList


urlpatterns = patterns('src.apps.catalogue.views',

    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^product/(?P<pk>[^/]+)/$', DetailProductView.as_view(), name='product_detail'),
    url(r'^category/(?P<slug>[^/]+)/$', ProductList.as_view(), name='products_in_category'),

)
