from typing import Dict, Any

from django import forms
from django.core.exceptions import PermissionDenied
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
    def can_create(self, user, model):
        raise NotImplementedError()

    def can_search(self, user, model):
        raise NotImplementedError()

    def check_search_permission(self, user, model):
        if self.can_search(user, model):
            return
        raise PermissionDenied()

    def check_create_permission(self, user, model):
        if self.can_create(user, model):
            return
        raise PermissionDenied()
