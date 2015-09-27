# -*- coding: utf-8 -*-
from django.forms import ModelForm
from src.apps.catalogue.models import Product

class AddProductForm(ModelForm):
    class Meta:
        model = Product
        fields = 'title', 'category', 'price', 'description',


class UpdateProductForm(ModelForm):
    class Meta:
        model = Product
        fields = 'title', 'category', 'price', 'description',

