import http
import logging
from flask import jsonify, request

from model.address import Address
from schema.facility_schema import facility_list_schema
from services.facility_services import FacilityService
from utils.jwt import require_user_token
from utils.constants import ADMIN, PROVIDER, CUSTOMER_SERVICE, STUDY_MANAGER
from utils.validation import validate_request
from werkzeug.exceptions import BadRequest

class FacilitiesManager:
    def __init__(self):
        self.facility_service_obj = FacilityService()

    @require_user_token(ADMIN, STUDY_MANAGER)
    def add_facility(self, token):
        logging.debug("User: {} Adding a facility".format(token["user_email"]))

        """ Add address, Facility and assign address id to facility table """
        from schema.facility_schema import add_facility_schema
        from services.facility_services import FacilityService

        logging.info("Request Received to add facility")
        request_data = validate_request()
        address, facility_name, on_call_phone, external_facility_id = add_facility_schema.load(request_data)
        logging.debug(
            "User: {} with role: {} - adding new facility: {}::{}".format(token["user_email"], token["user_role"],
                                                                          facility_name, external_facility_id))
        logging.info("Facility Name: {}".format(facility_name))
        logging.info("Address Info: {}".format(address))
        facility_obj = FacilityService()

        # Check if facility already exists
        exists = facility_obj.check_facility_exists_by_external_id(external_facility_id)
        if exists:
            return (
                    {"message": "Facility ext_id:{} already exists".format(external_facility_id), "status_code": http.client.CONFLICT},
                    http.client.CONFLICT,
                )

        aid, fid = facility_obj.register_facility(address, facility_name, on_call_phone, external_facility_id)
        return (
            {"address_id": aid, "facility_id": fid, "external_facility_id": external_facility_id,
             "status_code": http.client.CREATED},
            http.client.CREATED,
        )

    @require_user_token(ADMIN, STUDY_MANAGER, CUSTOMER_SERVICE)
    def get_facilities_list(self, token):
        """Return a list of facilities"""
        """
        :return filtered facilities list
        """
        logging.debug("User: {} getting list of all facilities".format(token["user_email"]))
        facilities_list, total = self.facility_service_obj.list_all_facilities()

        return (
            {
                "total": total,
                "data": facilities_list,
                "status_code": http.client.OK,
            },
            http.client.OK,
        )

    @require_user_token(ADMIN, STUDY_MANAGER)
    def get_facility(self, token):
        """Return facility object"""
        """
        :return facility object in json
        """
        request_data = request.args
        facility_id = request_data["id"]
        facility = self.facility_service_obj.get_facility_by_id(facility_id)
        if facility is None:
            return jsonify({'message': 'Facility not found'}, http.client.NOT_FOUND)
        resp = dict()
        resp['name'] = facility.name
        address = Address.find_by_id(_id=facility.address_id)
        address_dict = None
        if address:
            address_dict = {
                "street_address_1": address.street_address_1,
                "street_address_2": address.street_address_2,
                "city": address.city,
                "state": address.state,
                "country": address.country,
                "postal_code": address.postal_code,
            }
        resp['facility_name'] = facility.name
        resp['id'] = facility.id
        resp['external_facility_id'] = facility.external_facility_id
        resp['updated_on'] = facility.updated_on
        resp['created_at'] = facility.created_at
        resp['address_id'] = facility.address_id
        resp['address'] = address_dict
        resp['on_call_phone'] = facility.on_call_phone
        return jsonify(resp), http.client.OK

    @require_user_token(ADMIN, STUDY_MANAGER)
    def update_facility(self, token):
        from schema.facility_schema import update_facility_schema
        from services.facility_services import FacilityService

        """Update a facility details"""
        logging.debug("User: {} updating details of a facility".format(token["user_email"]))

        facility_id = request.args.get("id")
        if facility_id is None:
            raise BadRequest("parameter id is missing")

        try:
            request_data = validate_request()
            address, facility_name, on_call_phone, external_facility_id = update_facility_schema.load(request_data)

            facility_svc = FacilityService()
            facility_svc.update_facility(facility_id, address, facility_name, on_call_phone, external_facility_id)
        except Exception as ex:
            return {"message": "Update failed. Please check logs for details"}, http.client.BAD_REQUEST

        return {"message": "Sucessfully updated"}, http.client.OK

    @require_user_token(ADMIN, CUSTOMER_SERVICE, STUDY_MANAGER, PROVIDER)
    def get_paginated_list(self, token):
        """
        :param :- page_number, record_per_page, name, external ID
        :return filtered patient list
        """

        request_data = validate_request()
        logging.debug(
            "User: {} with role: {} - is requesting a list of facilities".format(token["user_email"],
                                                                               token["user_role"]))
        filter_input = facility_list_schema.load(request_data)
        facilities, total = self.facility_service_obj.get_filtered_facilities(*filter_input)

        return (
            {
                "total": total,
                "page_number": filter_input[0],
                "record_per_page": filter_input[1],
                "data": facilities,
                "status_code": http.client.OK
            },
            http.client.OK,
        )
