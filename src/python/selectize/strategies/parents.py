from django.db.models import Manager

from selectize.reflection import get_parents
from . import SelectizeParentsStrategy


class DefaultParentStrategy(SelectizeParentsStrategy):
    def get_parents_data(self, manager: Manager, request, url_args, url_kwargs):
        parents_chain = get_parents(manager.model._meta)
        parents_data = {}
        for parents in parents_chain:
            for parent_name, parent_model in parents.items():
                if (parent_name + '__pk') in url_kwargs:
                    parents_data[parent_name] = parent_model.objects.get(
                        pk=url_kwargs[parent_name + '__pk']
                    )
        return parents_data
