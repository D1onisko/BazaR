# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from src.apps.dashboard.views import DashboardIndexView


urlpatterns = patterns('src.apps.dashboard.views',

    url(r'^accounts/profile/', DashboardIndexView.as_view(), name='dashboard_index'),

)
