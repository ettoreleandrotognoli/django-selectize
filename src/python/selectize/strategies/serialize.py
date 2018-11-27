import json
from typing import Dict

from django.forms import Form
from django.http import HttpResponse
from . import SelectizeRenderStrategy
from . import SelectizeSerializeStrategy


class JsonStrategy(SelectizeSerializeStrategy):
    def __init__(self, encoder=json.dumps, content_type="application/json; charset=utf-8"):
        self.encode = encoder
        self.content_type = content_type

    def serialize_item(self, render_strategy: SelectizeRenderStrategy, item) -> Dict:
        return {
            'id': item.pk,
            '__item__': render_strategy.render_selectize_item(item),
            '__option__': render_strategy.render_selectize_option(item)
        }

    def serialize_error(self, form: Form) -> HttpResponse:
        errors = dict(form.errors.items())
        data = self.encode(errors)
        return HttpResponse(data, content_type=self.content_type, status=400)

    def serialize_searched_items(self, render_strategy: SelectizeRenderStrategy, items) -> HttpResponse:
        data = list(self.serialize_item(render_strategy, it) for it in items)
        return HttpResponse(self.encode(data), content_type=self.content_type)

    def serialize_created_item(self, render_strategy: SelectizeRenderStrategy, item) -> HttpResponse:
        data = self.serialize_item(render_strategy, item)
        return HttpResponse(self.encode(data), content_type=self.content_type, status=201)
