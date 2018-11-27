import json

from django.forms import Form
from django.http import HttpResponse
from . import SelectizeSerializeStrategy


class JsonStrategy(SelectizeSerializeStrategy):
    def __init__(self, encoder=json.dumps, content_type="application/json; charset=utf-8"):
        self.encode = encoder
        self.content_type = content_type

    def serialize_error(self, form: Form) -> HttpResponse:
        errors = dict(form.errors.items())
        data = self.encode(errors)
        return HttpResponse(data, content_type=self.content_type, status=400)

    def serialize_searched_items(self, items) -> HttpResponse:
        data = list(it.selectize_serialize() for it in items)
        return HttpResponse(self.encode(data), content_type=self.content_type)

    def serialize_created_item(self, item) -> HttpResponse:
        data = item.selectize_serialize()
        return HttpResponse(self.encode(data), content_type=self.content_type, status=201)
