# -*- coding: utf-8 -*-

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django import template

from src.apps.catalogue import models

register = template.Library()


@register.inclusion_tag('apps/catalogue/inclusion/categories_list.html')
def menu_tag():

    return {

        'categories': models.Category.objects.filter(is_active=True)
    }


