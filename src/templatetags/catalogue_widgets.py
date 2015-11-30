# -*- coding: utf-8 -*-

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django import template
from django.db.models import Count

from src.apps.catalogue.models import Category, Product
import mptt

register = template.Library()

@register.inclusion_tag('apps/catalogue/inclusion/categories_list.html')



def menu_tag():

        categ = Category.objects.all()
        test = Category.objects.get(id=11)

        return {
        'categories': categ,
        'test': test,

    }

