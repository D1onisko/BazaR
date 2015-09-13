# -*- coding: utf-8 -*-
from django.views.generic import DetailView, TemplateView, ListView
from django.shortcuts import get_object_or_404, redirect

from annoying.decorators import render_to, render_to_response
from pure_pagination.mixins import PaginationMixin
import mptt

from src.apps.catalogue.models import Category, Product

# Index page
class IndexView(PaginationMixin, ListView):
    template_name = 'apps/catalogue/index.html'
    model = Product
    paginate_by = 3

    def get_queryset(self):
        """ возврощяет все обьекты Product """
        return Product.objects.all()


# Detail page
class DetailProductView(DetailView):
    template_name = 'apps/catalogue/product_detail.html'
    model = Product
    context_object_name = 'product_vivod'


# Product in category
class ProductList(PaginationMixin, ListView):
    template_name = 'apps/catalogue/products_in_category.html'
    model = Product
    paginate_by = 2

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs['slug'])

        # filter product in child category
        if category.is_child_node():
            return Product.objects.filter(category_id=category.pk)

        # view all product in root category
        elif category.is_root_node():
            q = category.get_children()
            t = q.values('id')
            x = [item['id'] for item in t]
            return Product.objects.filter(category_id__in=x)

