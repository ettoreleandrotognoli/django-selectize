from typing import Dict

from django.conf import settings

from .reflection import get_parents
from .strategies import SelectizeCreateStrategy
from .strategies import SelectizeFilterStrategy
from .strategies import SelectizeParentsStrategy
from .strategies import SelectizePermissionStrategy
from .strategies import SelectizeRenderStrategy
from .strategies import SelectizeSearchStrategy
from .strategies import SelectizeSerializeStrategy
from .strategies.filter import DefaultFilterStrategy
from .strategies.parents import DefaultParentStrategy
from .strategies.permission import DjangoPermissionsStrategy
from .strategies.serialize import JsonStrategy

SELECTIZE_ATTR = getattr(settings, 'SELECTIZE_ATTR', '_selectize_')
SELECTIZE_OPTION_METHOD = getattr(settings, 'SELECTIZE_OPTION_METHOD', 'selectize_option')
SELECTIZE_ITEM_METHOD = getattr(settings, 'SELECTIZE_ITEM_METHOD', 'selectize_item')
SELECTIZE_SERIALIZE_METHOD = getattr(settings, 'SELECTIZE_SERIALIZE_METHOD', 'selectize_serialize')


class SelectizeModelMixin(object):
    def selectize_option(self) -> str:
        raise NotImplementedError()

    def selectize_item(self) -> str:
        raise NotImplementedError()

    def selectize_serialize(self) -> Dict:
        raise NotImplementedError()


def _selectize_option(self) -> str:
    return getattr(self, SELECTIZE_ATTR).render_strategy.render_selectize_option(self)


def _selectize_item(self) -> str:
    return getattr(self, SELECTIZE_ATTR).render_strategy.render_selectize_item(self)


def _selectize_serialize(self) -> Dict:
    return {
        'id': self.id,
        '__item__': getattr(self, SELECTIZE_ITEM_METHOD)(),
        '__option__': getattr(self, SELECTIZE_OPTION_METHOD)()
    }


class Selectize(object):
    def __init__(
            self,
            render_strategy: SelectizeRenderStrategy,
            search_strategy: SelectizeSearchStrategy,
            create_strategy: SelectizeCreateStrategy = None,
            filter_strategy: SelectizeFilterStrategy = None,
            serialize_strategy: SelectizeSerializeStrategy = None,
            permission_strategy: SelectizePermissionStrategy = None,
            parents_strategy: SelectizeParentsStrategy = None,
    ):
        self.render_strategy = render_strategy
        self.search_strategy = search_strategy
        self.create_strategy = create_strategy if create_strategy is not None else search_strategy.as_create_strategy()
        self.filter_strategy = filter_strategy if filter_strategy is not None else DefaultFilterStrategy()
        self.serialize_strategy = serialize_strategy if serialize_strategy is not None else JsonStrategy()
        self.permission_strategy = permission_strategy if permission_strategy is not None else DjangoPermissionsStrategy()
        self.parents_strategy = parents_strategy if parents_strategy is not None else DefaultParentStrategy()

    def __call__(self, model):
        parents = get_parents(model._meta)
        setattr(model, SELECTIZE_ATTR, self)
        setattr(model, SELECTIZE_OPTION_METHOD, _selectize_option)
        setattr(model, SELECTIZE_ITEM_METHOD, _selectize_item)
        setattr(model, SELECTIZE_SERIALIZE_METHOD, _selectize_serialize)
        return model
