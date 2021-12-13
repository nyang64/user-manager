import http
import logging

from schema.material_request_schema import add_materials_schema, material_list_schema
from services.material_request_services import MaterialRequestService
from utils.constants import ADMIN, CUSTOMER_SERVICE, STUDY_MANAGER
from utils.jwt import require_user_token
from utils.validation import validate_request


class MaterialsManager:
    def __init__(self):
        self.svc = MaterialRequestService()

    @require_user_token(ADMIN, CUSTOMER_SERVICE, STUDY_MANAGER)
    def generate_material_request(self, token):
        req_data = validate_request()
        # logging.debug(
        #     "User: {} with role: {} - is requesting new material request".format(token["user_email"],
        #                                                                          token["user_role"]))
        filtered_input = add_materials_schema.load(req_data)
        self.svc.send_new_product_request(request_data=filtered_input,
                                          logged_in_user_email=token["user_email"])
        return (
            {
                "status_code": http.client.OK
            },
            http.client.OK,
        )

    @require_user_token(ADMIN, CUSTOMER_SERVICE, STUDY_MANAGER)
    def get_paginated_list(self, token):
        """
        :param :- page_number, record_per_page, request_number
        :return filtered patient list
        """
        request_data = validate_request()
        logging.debug(
            "User: {} with role: {} - is requesting a list of material requests".format(token["user_email"],
                                                                                 token["user_role"]))
        filter_input = material_list_schema.load(request_data)
        data_list, total = self.svc.get_filtered_material_list(*filter_input)

        return (
            {
                "total": total,
                "page_number": filter_input[0],
                "record_per_page": filter_input[1],
                "data": data_list,
                "status_code": http.client.OK
            },
            http.client.OK,
        )