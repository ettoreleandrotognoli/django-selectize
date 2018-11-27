from django.db.models import Manager
from . import SelectizeFilterStrategy
from ..reflection import get_parents


class DefaultFilterStrategy(SelectizeFilterStrategy):
    def get_queryset(self, manager: Manager, request, url_args, url_kwargs):
        return manager.all().filter(**url_kwargs)

