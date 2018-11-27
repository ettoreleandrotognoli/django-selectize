from django.views import View

from .models import SELECTIZE_ATTR
from .models import Selectize
from .reflection import get_parents
from .strategies import SelectizeCreateStrategy
from .strategies import SelectizeFilterStrategy
from .strategies import SelectizeParentsStrategy
from .strategies import SelectizePermissionStrategy
from .strategies import SelectizeRenderStrategy
from .strategies import SelectizeSearchStrategy
from .strategies import SelectizeSerializeStrategy


class SelectizeView(View):
    content_type = "application/json; charset=utf-8"
    model = None
    selectize = None

    def __init__(self, model, parents=None, selectize: Selectize = None):
        self.model = model
        self.parents = parents if parents else get_parents(model._meta)
        self.selectize = selectize if selectize else getattr(model, SELECTIZE_ATTR)

    def get_manager(self):
        return self.model.objects

    def get_queryset(self):
        return self.get_filter_strategy().get_queryset(
            self.model.objects,
            self.request,
            self.args,
            self.kwargs,
        )

    def get_filter_strategy(self) -> SelectizeFilterStrategy:
        return self.selectize.filter_strategy

    def get_search_strategy(self) -> SelectizeSearchStrategy:
        return self.selectize.search_strategy

    def get_create_strategy(self) -> SelectizeCreateStrategy:
        return self.selectize.create_strategy

    def get_render_strategy(self) -> SelectizeRenderStrategy:
        return self.selectize.render_strategy

    def get_serialize_strategy(self) -> SelectizeSerializeStrategy:
        return self.selectize.serialize_strategy

    def get_permission_strategy(self) -> SelectizePermissionStrategy:
        return self.selectize.permission_strategy

    def get_parents_strategy(self) -> SelectizeParentsStrategy:
        return self.selectize.parents_strategy

    def get_form(self):
        if self.request.method in ('GET',):
            search_strategy = self.get_search_strategy()
            return search_strategy.get_form(self.request)
        elif self.request.method in ('POST',):
            create_strategy = self.get_create_strategy()
            return create_strategy.get_form(self.request)
        raise Exception()

    def check_permission(self):
        permission_strategy = self.get_permission_strategy()
        if self.request.method in ('GET',):
            return permission_strategy.check_search_permission(self.model)
        elif self.request.method in ('POST',):
            return permission_strategy.check_create_permission(self.model)
        raise Exception()

    def dispatch(self, request, *args, **kwargs):
        self.check_permission()
        form = self.get_form()
        if not form.is_valid():
            return self.get_serialize_strategy().serialize_error(form)
        return super().dispatch(request, form.cleaned_data, *args, **kwargs)

    def get(self, request, data, *args, **kwargs):
        search_strategy = self.get_search_strategy()
        result = search_strategy.search(self.get_queryset(), data)
        return self.get_serialize_strategy().serialize_searched_items(result)

    def post(self, request, data, *args, **kwargs):
        create_strategy = self.get_create_strategy()
        parents = self.get_parents_strategy().get_parents_data(self.get_manager(), request, args, kwargs)
        result = create_strategy.create(self.get_manager(), {**data, **parents})
        return self.get_serialize_strategy().serialize_created_item(result)
