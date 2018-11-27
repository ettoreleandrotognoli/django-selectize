from itertools import chain

from django.db.models.fields.related import ForeignKey
from django.db.models.options import Options


def fk_field(field):
    return isinstance(field, ForeignKey)


def not_null_field(field):
    return not field.null

def get_reversed_parent_fields(django_meta: Options):
    pass


def get_reverserd_parents_chain(django_meta: Options):
    visited_models = set()
    parents_chain = []
    parent_fields = get_parent_fields(django_meta)
    while not set(parent_fields.values()).issubset(visited_models):
        parents_chain.append(parent_fields)
        meta_list = map(lambda it: it._meta, parent_fields.values())
        parent_fields = dict(chain(*list(map(lambda it: it.items(), map(get_parent_fields, meta_list)))))
    return parents_chain[::-1]


def get_parent_fields(django_meta: Options):
    parent_fields = filter(not_null_field, filter(fk_field, django_meta.fields))
    relations = {}
    for field in parent_fields:
        relations[field.name] = field.target_field.model
    return relations


def get_parents(django_meta: Options):
    visited_models = set()
    parents_chain = []
    parent_fields = get_parent_fields(django_meta)
    while not set(parent_fields.values()).issubset(visited_models):
        parents_chain.append(parent_fields)
        meta_list = map(lambda it: it._meta, parent_fields.values())
        parent_fields = dict(chain(*list(map(lambda it: it.items(), map(get_parent_fields, meta_list)))))
    return parents_chain
