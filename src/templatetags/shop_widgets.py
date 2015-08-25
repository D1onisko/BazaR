# -*- coding: utf-8 -*-

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django import template
from django.db.models import Count, Max, Avg

from src.apps.catalogue import models

register = template.Library()


@register.inclusion_tag('apps/catalogue/inclusion/categories_list.html')
def categories_list_tag():

    return {

        'categories': models.Category.objects.filter(is_active=True)
    }

