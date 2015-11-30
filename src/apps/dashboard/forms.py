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
Выбор валюты
"""
GRIVNA, DOLLAR, = u'гривна', u'доллар'
STRUCTURE_CHOICES = (
    (GRIVNA, u'грн.'),
    (DOLLAR, u'$'),)


"""
Base fields in forms
"""
class BaseFields(forms.Form):

    category = SelectCategory(queryset=Category.objects.exclude(level=0),
                              label=u'Категория',
                              help_text=u'Выберите категорию: "Мобильные телефоны"')
    title = forms.CharField(label=u'Тема объявления',
                            help_text=u'Введите название объявления: "Продам козу"',
                            )
    price = forms.IntegerField(label=u'Цена',
                               required=True,
                               error_messages={'required': u'Это поле должно быть заполнено.'},
                               help_text=u'Введите цену',
                               )
    valuta = forms.ChoiceField(initial=GRIVNA, choices=STRUCTURE_CHOICES, label=False, widget=forms.RadioSelect(),
                               required=False)
    phone = forms.IntegerField(label=u'Номер телефона',
                               required=False,
                               error_messages={'required': u'Это поле должно быть заполнено.'},
                               help_text=u'Введите номер телефона')

    description = forms.CharField(widget=forms.Textarea(attrs={'rows': '8'}), label=u'Текст объявления',
                                  )


"""
class adds products in dashboard
"""

class AddProductForm(ModelForm, BaseFields):
    class Meta:
        model = Product
        fields = 'category', 'title', 'description', 'price', 'valuta', \
                 'phone', 'image',


"""
class Update dashboard
"""


class UpdateProductForm(ModelForm, BaseFields):
    class Meta:
        model = Product
        fields = 'title', 'category', 'description', 'price', 'valuta', \
                 'phone',
