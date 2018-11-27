import json
from typing import Iterable

from django.forms import widgets
from django.forms.utils import flatatt
from django.urls import reverse_lazy
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .reflection import get_parents


class SelectizeMixin(object):
    def __init__(self, *args, **kwargs):
        attrs = kwargs.get('attrs', {})
        attrs['selectize'] = attrs.get('selectize', 'selectize')
        for k, v in kwargs.pop('selectize', {}).items():
            attrs['selectize-%s' % k] = v
        kwargs['attrs'] = attrs
        super(SelectizeMixin, self).__init__(*args, **kwargs)


class EagerSelectizeMixin(SelectizeMixin):
    pass


class EagerSelectize(EagerSelectizeMixin, widgets.Select):
    pass


class MultipleEagerSelectize(EagerSelectizeMixin, widgets.SelectMultiple):
    pass


class RemoteSelectizeMixin(SelectizeMixin):
    multiple = None

    @classmethod
    def from_model(cls, model, **options):
        model_id = tuple(model._meta.label_lower.split('.'))
        parents_chain = get_parents(model._meta)
        url_kwargs = {}
        for parents in parents_chain:
            for parent_name, parent_model in parents.items():
                parent_model_id = tuple(parent_model._meta.label_lower.split('.'))
                url_kwargs['{}__pk'.format(parent_name)] = '<{}-{}>'.format(*parent_model_id)
        url = reverse_lazy(
            'selectize:selectize-{}-{}'.format(*model_id),
            kwargs=url_kwargs
        )
        return cls(
            href=url,
            selectize=dict(
                create=url
            ),
            attrs=options.get('attrs', {})
        )

    def __init__(self, *args, **kwargs):
        attrs = kwargs.get('attrs', {})
        attrs.update({
            'selectize': 'remote',
            'href': kwargs.pop('href', '')
        })
        kwargs['attrs'] = attrs
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, dict(name=name))
        objects = self.choices.queryset.filter(pk__in=value if isinstance(value, Iterable) else [value])
        final_attrs['selectize-options'] = json.dumps([obj.selectize_serialize() for obj in objects])
        final_attrs['selectize-items'] = json.dumps([obj.pk for obj in objects])
        if self.multiple:
            final_attrs['multiple'] = 'multiple'
        output = [format_html('<select{}>', flatatt(final_attrs))]
        output.append('</select>')
        return mark_safe('\n'.join(output))

    def render_options(self, choices, selected_choices):
        self.choices.queryset = self.choices.queryset.filter(pk__in=map(int, filter(None, selected_choices)))
        return super(RemoteSelectizeMixin, self).render_options(choices, selected_choices)


class RemoteSelectize(RemoteSelectizeMixin, widgets.Select):
    multiple = False


class MultipleRemoteSelectize(RemoteSelectizeMixin, widgets.SelectMultiple):
    multiple = True
