from django.apps import AppConfig

from selectize.models import SELECTIZE_ATTR
from .sites import SelectizeSite

site = SelectizeSite()


class SelectizeAppConfig(AppConfig):
    name = "selectize"

    def ready(self):
        self.module.autodiscover()
        for app, models in self.apps.all_models.items():
            for model_name, model_class in models.items():
                if not getattr(model_class, SELECTIZE_ATTR, False):
                    continue
                site.register((app, model_name), model_class)
