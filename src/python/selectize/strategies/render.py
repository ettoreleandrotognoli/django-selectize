from typing import Any

from django.template.loader import render_to_string
from . import SelectizeRenderStrategy


class DjangoTemplateStrategy(SelectizeRenderStrategy):
    DEFAULT_ITEM_TEMPLATE = '{}/selectize/item.html'
    DEFAULT_OPTION_TEMPLATE = '{}/selectize/option.html'

    def __init__(
            self,
            entity_name: str = None,
            item_template: str = DEFAULT_ITEM_TEMPLATE,
            option_template: str = DEFAULT_OPTION_TEMPLATE):
        self.entity_name = entity_name
        self.item_template = item_template
        self.option_template = option_template

    def render_selectize_option(self, entity: Any) -> str:
        return render_to_string(
            self.option_template.format(self.entity_name),
            dict(object=entity)
        )

    def render_selectize_item(self, entity: Any) -> str:
        return render_to_string(
            self.item_template.format(self.entity_name),
            dict(object=entity)
        )
