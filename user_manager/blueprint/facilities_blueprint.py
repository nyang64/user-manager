from flask import Blueprint
from resources.facilities_manager import FacilitiesManager


class FacilitiesBlueprint(Blueprint):
    def __init__(self):
        super().__init__(__class__.__name__, __name__)
        self.facilities_obj = FacilitiesManager()
        self._add_routes()

    def _add_routes(self):
        self.add_url_rule(
            "/add/facility",
            "Add Facility",
            self.facilities_obj.add_facility,
            methods=["POST"],
        )
        self.add_url_rule(
            "/facilities",
            "List all facilities",
            self.facilities_obj.get_facilities_list,
            methods=["GET"]
        )

        # Used by:
        # patient management portal: add/edit facilities
        self.add_url_rule(
            "/facilities_providers",
            "List all facilities and providers",
            self.facilities_obj.get_facilities_providers,
            methods=["GET"]
        )

        # Used by:
        # patient management portal: sites list
        self.add_url_rule(
            "/facilities/list",
            "Paginated list of facilities",
            self.facilities_obj.get_paginated_list,
            methods=["POST"]
        )
        self.add_url_rule(
            "/facilities/update",
            "Update a facility",
            self.facilities_obj.update_facility,
            methods=["PUT"]
        )
        self.add_url_rule(
            "/facility/detail",
            "Get a facility",
            self.facilities_obj.get_facility,
            methods=["GET"],
        )

        # Used by:
        # patient management portal: view/edit facilities
        self.add_url_rule(
            "/facilities/facility_providers",
            "Get facility details along with outpatient provider and site coordinators",
            self.facilities_obj.get_facility_and_providers,
            methods=["GET"]
        )
