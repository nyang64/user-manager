from flask import Blueprint
from admin.operations.admin_operations import admin_manager


class AdminBlueprint(Blueprint):
    def __init__(self):
        super().__init__(__class__.__name__, __name__)
        self.admin_obj = admin_manager()
        self._add_routes()

    def _add_routes(self):
        self.add_url_rule('/admin/register',
                          'Register Admin',
                          self.admin_obj.register_admin,
                          methods=['POST'])
