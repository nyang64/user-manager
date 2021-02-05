from flask import Blueprint
from admin.operations.admin_operations import admin_manager


class AdminBlueprint(Blueprint):
    def __init__(self):
        super().__init__(__class__.__name__, __name__)
        self.admin_obj = admin_manager()
        self._add_routes()

    def _add_routes(self):
        self.add_url_rule('/seed/db',
                          'seed db',
                          self.admin_obj.seed_db,
                          methods=['POST']
                          )
