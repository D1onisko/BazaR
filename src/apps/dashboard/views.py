# -*- coding: utf-8 -*-
from django.views.generic import DetailView, TemplateView, ListView, View
from django.shortcuts import get_object_or_404, redirect
from annoying.decorators import render_to
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger, PaginationMixin


import mptt

from src.apps.catalogue.models import Category, Product



# Index page
class DashboardIndexView(TemplateView):
    template_name = 'apps/dashboard/profile.html'
    model = Product

    def get(self, request, *args, **kwargs):
        kwargs['object_list'] = Product.objects.filter(user_name_id=request.user)
        return super(DashboardIndexView, self).get(request, *args, **kwargs)

