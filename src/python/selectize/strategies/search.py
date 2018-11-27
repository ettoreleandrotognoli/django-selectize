from functools import reduce
from operator import or_
from typing import Iterable

from django import forms
from django.db.models import Q
from . import SelectizeSearchStrategy, SelectizeCreateStrategy


class SelectizeSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
    )


class SearchFieldsStrategy(SelectizeSearchStrategy):
    form_class = SelectizeSearchForm

    def __init__(self, fields: Iterable[str], lookup='icontains', limit=10):
        self.fields = tuple(fields)
        self.lookup = lookup
        self.limit = limit

    def get_form(self, request):
        return self.form_class(data=request.GET)

    def search(self, queryset, data):
        search_value = data.get('q', None)
        if search_value is None:
            return queryset
        filter_query = reduce(or_, [Q(**{'{}__{}'.format(f, self.lookup): search_value}) for f in self.fields])
        return queryset.filter(filter_query)[0:self.limit]

    def as_create_strategy(self) -> SelectizeCreateStrategy:
        from .create import SearchFieldsStrategyAdapter
        return SearchFieldsStrategyAdapter(self)
