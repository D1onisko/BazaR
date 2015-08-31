# -*- coding: utf-8 -*-
from django.views.generic import DetailView, TemplateView, ListView
from annoying.decorators import render_to
from django.shortcuts import get_object_or_404, redirect

from src.apps.catalogue.models import Category, Product

# Index page
class IndexView(ListView):
    template_name = 'apps/catalogue/index.html'
    context_object_name = 'index_list_all'

    def get_queryset(self):
        """ возврощяет все обьекты Product """
        return Product.objects.all()


#  Detail page
class DetailProductView(DetailView):
    model = Product
    template_name = 'apps/catalogue/detail.html'
    context_object_name = 'product_vivod'


# меню сайта
@render_to('apps/catalogue/category_all_item.html')
def category(request, slug):
    current_category = get_object_or_404(Category, slug=slug)

    # вывод всех продуктов категории

    # фильтрация продуктов определенной одной категории
    category_vivod = Product.objects.filter(category_id=current_category.pk)
    return dict(current_category=current_category,
                category_vivod=category_vivod,
                )
