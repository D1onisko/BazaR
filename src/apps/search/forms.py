# encoding: utf-8
from django import forms
from haystack.forms import HighlightedModelSearchForm
from haystack.query import SearchQuerySet

from src.apps.catalogue.models import Product

class ProductSearchForm(HighlightedModelSearchForm):
    products = forms.ModelChoiceField(queryset=Product.objects.all(), required=False)

    def search(self):

        # First, store the SearchQuerySet received from other processing.
        sqs = super(ProductSearchForm, self).search()

        if not self.is_valid():
            return self.no_query_found()

        if self.cleaned_data['products']:
            sqs = sqs.filter(products=self.cleaned_data['products'])

        return sqs

