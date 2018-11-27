from typing import Dict, Any

from django import forms
from django.db.models import QuerySet, Manager
from django.http import HttpResponse


class SelectizeSerializeStrategy(object):
    def serialize_error(self, form: forms.Form) -> HttpResponse:
        raise NotImplementedError()

    def serialize_created_item(self, item) -> HttpResponse:
        raise NotImplementedError()

    def serialize_searched_items(self, items) -> HttpResponse:
        raise NotImplementedError()


class SelectizeRenderStrategy(object):
    entity_name = None

    def render_selectize_option(self, entity) -> str:
        raise NotImplementedError()

    def render_selectize_item(self, entity) -> str:
        raise NotImplementedError()


class SelectizeFilterStrategy(object):
    def get_queryset(self, manager: Manager, request, url_args, url_kwargs) -> QuerySet:
        raise NotImplementedError()


class SelectizeParentsStrategy(object):
    def get_parents_data(self, manager: Manager, request, url_args, url_kwargs) -> Dict:
        raise NotImplementedError()


class SelectizeSearchStrategy(object):
    def get_form(self, request) -> forms.Form:
        raise NotImplementedError()

    def search(self, queryset: QuerySet, data: Dict) -> QuerySet:
        raise NotImplementedError()


class SelectizeCreateStrategy(object):
    def get_form(self, request) -> forms.Form:
        raise NotImplementedError()

    def create(self, manager: Manager, data: Dict) -> Any:
        raise NotImplementedError()


class SelectizePermissionStrategy(object):
    def check_search_permission(self, model):
        raise NotImplementedError()

    def check_create_permission(self, model):
        raise NotImplementedError()
