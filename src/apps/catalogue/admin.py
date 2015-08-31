# -*- coding: utf-8 -*-
from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin

from src.apps.catalogue import models


class ProductAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_created'
    list_display = ('title', 'category', 'date_created')
    list_filter = ['is_discountable']
    search_fields = ['title']



class CategoryAdmin(DjangoMpttAdmin):
    list_display = ('name', 'is_active')
    fieldsets = ((None, {'fields': ('name', 'is_active', 'parent', 'structure')}), )
    search_fields = ('name',)
    mptt_level_indent = 20

admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Category, CategoryAdmin)
