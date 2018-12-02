from distutils import version
from . import SelectizePermissionStrategy
from ..reflection import get_model_id




class AllowAllStrategy(SelectizePermissionStrategy):
    def check_search_permission(self, *args, **kwargs):
        return

    def check_create_permission(self, *args, **kwargs):
        return


DJANGO_DEFAULT_PERMISSIONS = {
    'search': [],
    'create': ['{}.add_{}']
}

DJANGO_PlUS_VIEW_PERMISSIONS = {
    'search': ['{}.view_{}'],
    'create': ['{}.add_{}'],
}


class DjangoPermissionsStrategy(SelectizePermissionStrategy):
    def __init__(self, permissions=DJANGO_DEFAULT_PERMISSIONS):
        self.permissions = permissions

    def can_search(self, user, model):
        model_id = get_model_id(model)
        permissions = map(lambda it: it.format(*model_id), self.permissions['search'])
        return user.has_perms(permissions)

    def can_create(self, user, model):
        model_id = get_model_id(model)
        permissions = map(lambda it: it.format(*model_id), self.permissions['create'])
        return user.has_perms(permissions)
