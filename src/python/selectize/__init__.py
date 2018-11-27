from django.utils.module_loading import autodiscover_modules

default_app_config = "selectize.apps.SelectizeAppConfig"


def autodiscover():
    autodiscover_modules('selectize')
