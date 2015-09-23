# encoding: utf-8
from django import forms
from haystack.forms import SearchForm


class DateRangeSearchForm(SearchForm):

    def search(self):

        # First, store the SearchQuerySet received from other processing.
        sqs = super(DateRangeSearchForm, self).search()

        if not self.is_valid():
            return self.no_query_found()

        return sqs

