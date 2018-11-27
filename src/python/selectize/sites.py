from typing import Tuple

from django import forms
from django.shortcuts import render
from django.views import View
from django.views.decorators import csrf
from selectize.models import SELECTIZE_ATTR
from selectize.models import SELECTIZE_DEFAULT
from . import widgets
from .reflection import get_parents
from .views import SelectizeView


class SelectizeSite(object):
    def __init__(self, name="selectize", registered_models={}):
        self.name = name
        self.registered_models = registered_models

    def register(self, model_id: Tuple[str, str], model_class):
        self.registered_models[model_id] = model_class

    def as_name(self, model_id: Tuple[str, str]) -> str:
        return 'selectize-{}-{}'.format(*model_id)

    def as_path(self, model_id: Tuple[str, str], model) -> str:
        parents_chain = get_parents(model._meta)[::-1]
        url_prefix = '^{}/'.format(model_id[0])
        for parents in parents_chain:
            for parent_name, parent_model in parents.items():
                url_prefix += r'{}/(?P<{}__pk>.+)/'.format(parent_name, parent_name)
        return url_prefix + ('{}/$'.format(model_id[1]))

    def as_view(self, model_id: Tuple[str, str], model):
        selectizes = getattr(model, SELECTIZE_ATTR, {})
        return csrf.csrf_exempt(SelectizeView.as_view(model=model, selectize=selectizes[SELECTIZE_DEFAULT]))

    def make_urls(self):
        from django.conf.urls import url
        urlpatterns = list(
            url(self.as_path(model_id, model), self.as_view(model_id, model), name=self.as_name(model_id))
            for model_id, model in self.registered_models.items()
        )
        return urlpatterns

    def make_preview_form_class(self, model_id, model):
        parents_chain = get_parents(model._meta)
        listen_attrs = {}
        for parents in parents_chain:
            for parent_name, parent_model in parents.items():
                parent_id = tuple(parent_model._meta.label_lower.split('.'))
                listen_attrs['listen-{}-{}'.format(*parent_id)] = "selectize-search-url selectize-create-url"

        class PreviewForm(forms.Form):
            prefix = '{}-{}'.format(*model_id)
            one_remote = forms.ModelChoiceField(
                label='Select one "{}"'.format(model.__name__),
                help_text="Remote",
                queryset=model.objects.all(),
                widget=widgets.RemoteSelectize.from_model(model, attrs={
                    'model': prefix,
                    **listen_attrs
                }),
                required=False,
            )
            many_remote = forms.ModelMultipleChoiceField(
                label='Select many "{}"'.format(model.__name__),
                help_text="Remote",
                queryset=model.objects.all(),
                widget=widgets.MultipleRemoteSelectize.from_model(model, attrs={
                    **listen_attrs
                }),
                required=False,
            )
            one_eager = forms.ModelChoiceField(
                label='Select one "{}"'.format(model.__name__),
                help_text="Eager",
                queryset=model.objects.all(),
                widget=widgets.EagerSelectize(),
                required=False,
            )
            many_eager = forms.ModelMultipleChoiceField(
                label='Select many "{}"'.format(model.__name__),
                help_text="Eager",
                queryset=model.objects.all(),
                widget=widgets.MultipleEagerSelectize(),
                required=False,
            )

        return PreviewForm

    def make_preview_view(self):
        class PreviewView(View):
            form_classes = tuple(
                self.make_preview_form_class(model_id, model) for model_id, model in self.registered_models.items()
            )

            def get_forms(self, data=None):
                return tuple(form_class(data=data) for form_class in self.form_classes)

            def get(self, request, *args, **kwargs):
                form_list = self.get_forms(None)
                return render(request, 'preview.html', {'form_list': form_list})

            def post(self, request, *args, **kwargs):
                form_list = self.get_forms(request.POST)
                for form in form_list:
                    form.is_valid()
                return render(request, 'preview.html', {'form_list': form_list})

        return PreviewView

    def make_preview_urls(self):
        from django.conf.urls import url
        urlpatterns = [
            url('^$', self.make_preview_view().as_view(), name="preview"),
        ]
        return urlpatterns

    @property
    def urls(self):
        return self.make_urls(), "selectize", self.name

    @property
    def preview_urls(self):
        return self.make_preview_urls(), "selectize-preview", self.name


def urls():
    from .apps import site
    return site.urls


def preview_urls():
    from .apps import site
    return site.preview_urls
