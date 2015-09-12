# -*- coding: utf-8 -*-
from django.views.generic import DetailView, TemplateView, ListView
from annoying.decorators import render_to
from django.shortcuts import get_object_or_404, redirect

from src.apps.catalogue.models import Category, Product
import mptt

# Index page
class IndexView(ListView):
    template_name = 'apps/catalogue/index.html'
    context_object_name = 'view_all_products'

    def get_queryset(self):
        """ возврощяет все обьекты Product """
        return Product.objects.all()


# Detail page
class DetailProductView(DetailView):
    model = Product
    template_name = 'apps/catalogue/product_detail.html'
    context_object_name = 'product_vivod'


# меню сайта
@render_to('apps/catalogue/products_in_category.html')
def products_in_category(request, slug):
    current_category = get_object_or_404(Category, slug=slug)
    # фильтрация продуктов определенной категории
    category_vivod = Product.objects.filter(category_id=current_category.pk)
    return dict(category_vivod=category_vivod)


@render_to('apps/catalogue/all_products_in_category.html')
def all_products_in_root_category(request, slug):
    current_category = get_object_or_404(Category, slug=slug)
    # выборка и запись в список id товара
    q = current_category.get_children()
    test = q.values('id')
    ix = [item['id'] for item in test]
    # фильтрация всех продуктов определенной категории
    category_vivod_all = Product.objects.filter(category_id__in=ix)
    return dict(test=ix,
                category_vivod_all=category_vivod_all,
                )
