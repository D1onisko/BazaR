# -*- coding: utf-8 -*-
from django.views.generic import DetailView, TemplateView
from annoying.decorators import render_to

from src.apps.catalogue.models import Category, Product


@render_to('apps/catalogue/index.html')
def index(request):
    product_list = Product.objects.all()
    return {'product_list': product_list}


# вывод детального описания лота
@render_to('apps/catalogue/detail.html')
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return {'product': product}


# меню сайта
@render_to('apps/catalogue/category.html')
def category(request, slug):
    current_category = get_object_or_404(Category, slug=slug)
    root_category_id = current_category.get_root()
    # фильтрация продуктов определенной категории
    category_vivod = Product.objects.filter(category_id=current_category.pk)
    return dict(current_category=current_category,
                root_category_id=root_category_id,
                category_vivod=category_vivod)