# -*- coding: utf-8 -*-
from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin

from src.apps.catalogue import models

class ProductCategoryAdmin(admin.ModelAdmin):
    pass

class ProductAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_created'
    list_display = ('get_title', 'category', 'date_created')
    list_filter = ['structure', 'is_discountable']
    search_fields = ['title']



class CategoryAdmin(DjangoMpttAdmin):
    list_display = ('name', 'is_active', )
    fieldsets = ((None, {'fields': ('name', ('is_active',),)}), )
    search_fields = ('name',)
    mptt_level_indent = 20

admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductImage)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.ProductCategory, ProductCategoryAdmin)
