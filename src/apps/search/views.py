# -*- coding: utf-8 -*-
from haystack.generic_views import SearchView
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger, PaginationMixin

from .forms import ProductSearchForm


class ProductSearchView(PaginationMixin, SearchView):
    template_name = 'search/search.html'
    form_class = ProductSearchForm


