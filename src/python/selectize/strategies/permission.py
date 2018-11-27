from . import SelectizePermissionStrategy


class AllowAllStrategy(SelectizePermissionStrategy):
    def check_search_permission(self, *args, **kwargs):
        return

    def check_create_permission(self, *args, **kwargs):
        return


class DjangoPermissionsStrategy(SelectizePermissionStrategy):
    def check_search_permission(self, model):
        return

    def check_create_permission(self, model):
        return
