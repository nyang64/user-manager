from flask import Blueprint
from resources.materials_manager import MaterialsManager


class MaterialsBlueprint(Blueprint):
    def __init__(self):
        super().__init__(__class__.__name__, __name__)
        self.materials_obj = MaterialsManager()
        self._add_routes()

    def _add_routes(self):
        self.add_url_rule(
            "/materials",
            "Add Materials Request",
            self.materials_obj.generate_material_request,
            methods=["POST"],
        )

        self.add_url_rule(
            "/materials/list",
            "Return a list of paginated materials requests",
            self.materials_obj.get_paginated_list,
            methods=["POST"],
        )