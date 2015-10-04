# -*- coding: utf-8 -*-
from django.forms import ModelForm, ModelChoiceField
from django import forms
from itertools import groupby
from operator import attrgetter
import mptt

from src.apps.catalogue.models import Category, Product


"""
class Select for AddProductForm
"""

class SelectCategory(ModelChoiceField):
    def __init__(self, *args, **kwargs):
        super(SelectCategory, self).__init__(*args, **kwargs)

        # фильтрация по полю 'description'.для внесение новых пунктов требуется перезапустить сервер
        groups = groupby(kwargs['queryset'], attrgetter('description'))

        self.choices = [(continent, [(c.id, self.label_from_instance(c)) for c in countries])
                        for continent, countries in groups]

"""
Base fields in forms
"""
class BaseFields(forms.Form):
    category = SelectCategory(empty_label='---', queryset=Category.objects.exclude(level=0), label='Категория')
    title = forms.CharField(label='Название товара')
    price = forms.IntegerField(label='Цена')
    description = forms.CharField(widget=forms.Textarea, max_length=100, label='Описание')


"""
class adds products in dashboard
"""
class AddProductForm(ModelForm, BaseFields):

    class Meta:
        model = Product
        fields = 'title', 'category', 'price','phone','address', 'description', 'image',


"""
class Update dashboard
"""
class UpdateProductForm(ModelForm, BaseFields):

    class Meta:
        model = Product
        fields = 'title', 'category', 'price', 'phone','address','description','image',
