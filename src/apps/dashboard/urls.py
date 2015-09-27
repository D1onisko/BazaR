# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from src.apps.dashboard.views import DashboardIndexView, ProductCreate, ProductUpdate, ProductDelete


urlpatterns = patterns('src.apps.dashboard.views',

    url(r'^accounts/profile/', DashboardIndexView.as_view(), name='dashboard_index'),
    url(r'accounts/add/$', ProductCreate.as_view(), name='product_add'),
    url(r'accounts/(?P<pk>\d+)/update/$', ProductUpdate.as_view(), name='product_update'),
    url(r'accounts/(?P<pk>\d+)/delete/$', ProductDelete.as_view(), name='product_delete'),

)
