# encoding: utf-8
from django.utils import timezone
from haystack import indexes
from src.apps.catalogue.models import Product

class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    user = indexes.CharField(model_attr='user_name')
    date_created = indexes.DateField(model_attr='date_created')

    def get_model(self):
        return Product

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(date_updated__lte=timezone.now())
