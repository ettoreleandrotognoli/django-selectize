import os

from django.apps import apps
from django.core.management.base import BaseCommand
from selectize.models import SELECTIZE_ATTR

default_item = """
<span class="item">{{object}}</span>
""".strip()

default_option = """
<div class="option">
{{object}}
</div>
""".strip()

templates = {
    "item.html": default_item,
    "option.html": default_option,
}


class Command(BaseCommand):
    help = "Generete default templates for DjangoTemplateStrategy"

    def add_arguments(self, parser):
        pass

    def write_on_file(self, file, content):
        with open(file, "w+") as output:
            output.write(content)

    def handle(self, *args, **options):
        for app_name, app_models in apps.all_models.items():
            app = apps.get_app_config(app_name)
            base_path = app.path
            for model_name, model_class in app_models.items():
                selectize = getattr(model_class, SELECTIZE_ATTR, False)
                if not selectize:
                    continue
                for template_name, template_content in templates.items():
                    template_file_name = os.path.join(
                        base_path,
                        "templates",
                        model_name,
                        "selectize",
                        template_name
                    )
                    if os.path.isfile(template_file_name):
                        self.stdout.write(
                            self.style.WARNING("The template '{}' already exists ".format(template_file_name))
                        )
                        continue
                    os.makedirs(os.path.dirname(template_file_name), exist_ok=True)
                    self.write_on_file(template_file_name, template_content)
