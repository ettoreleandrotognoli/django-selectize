from typing import Any, Dict

from django import forms
from django.db.models import Manager
from . import SelectizeCreateStrategy
from .search import SearchFieldsStrategy


class SearchFieldsStrategyAdapter(SelectizeCreateStrategy):
    def __init__(self, search_strategy: SearchFieldsStrategy):
        self.search_strategy = search_strategy

    def get_form(self, request) -> forms.Form:
        return self.search_strategy.form_class(data=request.POST)

    def create(self, manager: Manager, data: Dict) -> Any:
        main_field = self.search_strategy.fields[0]
        data = dict(data)
        data[main_field] = data.pop('q')
        return manager.create(**data)


class FormCreateStrategy(SelectizeCreateStrategy):
    def __init__(self, form_class):
        self.form_class = form_class

    def get_form(self, request) -> forms.Form:
        return self.form_class(data=request.POST)

    def create(self, manager: Manager, data: Dict) -> Any:
        return manager.create(**data)
