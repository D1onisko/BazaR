# -*- coding: utf-8 -*-

from haystack.generic_views import SearchView
from .forms import DateRangeSearchForm


class JohnSearchView(SearchView):
    template_name = 'search/search.html'
    form_class = DateRangeSearchForm
    paginate_by = 2

