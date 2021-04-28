from flask import Blueprint
from resources.provider_manager import ProviderManager


class ProviderBlueprint(Blueprint):
    def __init__(self):
        super().__init__(__class__.__name__, __name__)
        self.provider_Obj = ProviderManager()
        self._add_routes()

    def _add_routes(self):
        self.add_url_rule(
            "/provider/register",
            "Register Provider",
            self.provider_Obj.register_provider,
            methods=["POST"],
        )
        self.add_url_rule(
            "/provider/get",
            "Get Provider",
            self.provider_Obj.get_provider_by_id,
            methods=["GET"],
        )
        self.add_url_rule(
            "/provider/delete",
            "Delete the Provider",
            self.provider_Obj.delete_provider,
            methods=["DELETE"],
        )
        self.add_url_rule(
            "/provider/update",
            "Update the Provider",
            self.provider_Obj.update_provider,
            methods=["PUT"],
        )
        self.add_url_rule(
            "/providers",
            "Get List of Providers",
            self.provider_Obj.get_providers,
            methods=["GET"],
        )
        self.add_url_rule(
            "/patients/list",
            "Get all patient list",
            self.provider_Obj.get_patient_list,
            methods=["POST"],
        )
        self.add_url_rule(
            "/patient/detail",
            "Get patient detail",
            self.provider_Obj.get_patient_detail_byid,
            methods=["GET"],
        )
        self.add_url_rule(
            "/patient/report",
            "Get report link",
            self.provider_Obj.get_report_signed_link,
            methods=["GET"],
        )
        self.add_url_rule(
            "/report/update",
            "Update uploaded ts",
            self.provider_Obj.update_uploaded_ts,
            methods=["POST"],
        )
        """------------------------ Facility Endpoint -------------------------"""
        self.add_url_rule(
            "/add/facility",
            "Add Facility",
            self.provider_Obj.add_facility,
            methods=["POST"],
        )
