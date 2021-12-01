import http
import logging

from flask import jsonify, request
from model.address import Address
from model.facilities import Facilities
from model.providers import Providers
from model.providers_roles import ProviderRoles
from model.user_registration import UserRegister
from model.users import Users
from schema.address_schema import AddressSchema
from schema.patient_schema import (
    filter_patient_schema,
    patient_detail_schema,
    patient_id_schema,
)
from schema.providers_roles_schema import ProvidersRolesSchema
from schema.providers_schema import ProvidersSchema, UpdateProviderSchema, provider_list_schema
from schema.register_schema import RegistrationSchema
from schema.report_schema import patient_reports_schema, report_id_schema
from schema.user_schema import UserSchema
from services.provider_services import ProviderService
from services.user_services import UserServices
from services.facility_services import FacilityService
from utils.common import have_keys
from utils.constants import ADMIN, PROVIDER, CUSTOMER_SERVICE, STUDY_MANAGER
from utils.jwt import require_user_token
from utils.validation import validate_request
from utils.common import generate_random_password
from utils.send_mail import send_provider_registration_email
from werkzeug.exceptions import BadRequest

provider_schema = ProvidersSchema()
providers_schema = ProvidersSchema(many=True)
providers_roles_schema = ProvidersRolesSchema(many=True)
address_schema = AddressSchema()
register_schema = RegistrationSchema()
user_schema = UserSchema()


class ProviderManager:
    def __init__(self):
        self.userObj = UserServices()
        self.provider_obj = ProviderService()
        self.facility_service_obj = FacilityService()

    @require_user_token(ADMIN, STUDY_MANAGER, CUSTOMER_SERVICE)
    def register_provider(self, token):
        provider_json = request.json
        if (
                have_keys(
                    provider_json,
                    "first_name",
                    "last_name",
                    "facility_id",
                    "email",
                    "role",
                )
                is False
        ):
            return {"message": "Invalid Request Parameters"}, 400

        logging.debug(
            "User: {} with role: {} - is registering a new provider: {}::{}".format(token["user_email"],
                                                                                    token["user_role"],
                                                                                    provider_json["first_name"],
                                                                                    provider_json["last_name"]))
        pwd = generate_random_password()
        register = (str(provider_json["email"]).lower(), pwd)

        phone_number = None
        if "phone_number" in provider_json:
            phone_number = provider_json["phone_number"]

        external_user_id = None
        if "external_user_id" in provider_json:
            external_user_id = provider_json["external_user_id"]

        user = (
            provider_json["first_name"],
            provider_json["last_name"],
            phone_number,
            external_user_id
        )

        facility_id = provider_json["facility_id"]
        role_name = provider_json["role"]
        provider_id = self.provider_obj.register_provider_service(
            register, user, facility_id, role_name
        )

        provider = Providers.find_by_id(provider_id)
        facility = Facilities.find_by_id(int(facility_id))
        address = Address.find_by_id(facility.address_id)
        provider_roles = ProviderRoles.find_by_provider_id(provider_id)
        user = Users.find_by_id(provider.user_id)
        registration = UserRegister.find_by_id(user.registration_id)

        send_provider_registration_email(
            first_name=user.first_name,
            last_name=user.last_name,
            to_address=registration.email,
            username=registration.email,
            password=pwd
        )

        response = {
            "registration": register_schema.dump(registration),
            "user": user_schema.dump(user),
            "provider_role": providers_roles_schema.dump(provider_roles),
            "facility": {
                "name": facility.name,
                "address": address_schema.dump(address),
                "on_call_phone": facility.on_call_phone,
            },
        }
        response.update(provider_schema.dump(provider))

        return response, 201

    @require_user_token(ADMIN, PROVIDER)
    def get_provider_by_id(self, decrypt):
        provider_id = request.args.get("id")
        provider = Providers.find_by_id(provider_id)
        if provider is None:
            return {"message": "No Such Provider Exist"}, 404
        user = Users.find_by_id(provider.user_id)
        facility = Facilities.find_by_id(provider.facility_id)
        registration = UserRegister.find_by_id(user.registration_id)
        provider_dict = {
            "id": provider.id,
            "external_id": user.external_user_id,
            "facility_id": provider.facility_id,
            "facility_name": facility.name,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone_number": user.phone_number,
            "email": registration.email,
        }
        return {"Data": [provider_dict]}, 200

    @require_user_token(ADMIN, CUSTOMER_SERVICE, STUDY_MANAGER, PROVIDER)
    def get_providers(self, decrypt):
        provider_data = Providers.find_providers()
        if provider_data is None or provider_data == []:
            return {"message": "No Providers Found"}, 404

        providers_lst = []
        for provider in provider_data:
            user = Users.find_by_id(provider.user_id)
            facility = Facilities.find_by_id(provider.facility_id)
            patients = self.provider_obj.list_all_patients_by_provider(provider_id=provider.id)
            provider_dict = {
                "id": provider.id,
                "user_id": provider.user_id,
                "facility_id": provider.facility_id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone_number": user.phone_number,
                "facility_name": facility.name,
                "patients": patients,
            }
            providers_lst.append(provider_dict)
        return {"message": "Users Found", "data": providers_lst}, 200

    @require_user_token(ADMIN)
    def delete_provider(self, decrypt):
        provider_json = request.json
        if have_keys(provider_json, "provider_id") is False:
            return {"message": "Invalid Request Parameters"}, 400
        provider_data = Providers.find_by_id(_id=provider_json["provider_id"])
        if provider_data is None:
            return {"message": "Unable To Delete, No Such Provider Exist"}, 404
        self.userObj.delete_user_byid(provider_data.user_id)
        return {"message": "Provider Deleted"}, 200

    @require_user_token(ADMIN, STUDY_MANAGER)
    def update_provider(self, token):
        """Update a facility details"""
        logging.debug("User: {} updating providers".format(token["user_email"]))

        provider_id = request.args.get("id")
        if provider_id is None:
            raise BadRequest("Provider id parameter is missing")

        try:
            request_data = validate_request()
            req_facility_id, req_email, req_user = UpdateProviderSchema.load(request_data)

            provider_data = Providers.find_by_id(_id=provider_id)
            if provider_data is None:
                return {"message": "No Such Provider Exist"}, 404

            self.provider_obj.update_provider(facility_id=req_facility_id,
                                              user=req_user,
                                              email=req_email,
                                              provider_from_db=provider_data)
        except Exception as ex:
            return {"message": ex.description}, http.client.BAD_REQUEST

        return {"message": "Successfully updated provider"}, http.client.OK

    @require_user_token(PROVIDER)
    def get_patient_list(self, token):
        """
        :param :- page_number, record_per_page, first_name,
                  last_name, date_of_birth, report_id
        :return filtered patient list
        """

        provider = Providers.find_by_email(token["user_email"])
        request_data = validate_request()
        filter_input = filter_patient_schema.load(request_data)
        patients_list, total = self.provider_obj.patients_list(
            provider.id, *filter_input
        )

        return (
            {
                "total": total,
                "page_number": filter_input[0],
                "record_per_page": filter_input[1],
                "data": patients_list,
                "status_code": http.client.OK,
            },
            http.client.OK,
        )

    @require_user_token(PROVIDER)
    def get_patient_detail_byid(self, token):
        """
        Fetch the patient detail by their patientid
        param: patientID
        return: patient detail in dict format
        """
        request_data = request.args
        patient_id = patient_id_schema.load(request_data).get("patientID")
        patient_data, reports = self.provider_obj.patient_detail_byid(patient_id)
        patient_data = patient_detail_schema.dump(patient_data)
        patient_data["report"] = patient_reports_schema.dump(reports)
        return jsonify(patient_data), http.client.OK

    @require_user_token(PROVIDER)
    def get_report_signed_link(self, token):
        """
        Fetch the key by reportid from Salvos Table and get the signed url
        param: reportId
        return: Report Signed URL
        """
        request_data = request.args
        report_id = report_id_schema.load(request_data).get("reportId")
        signed_url, code = self.provider_obj.report_signed_link(report_id)
        return {"report_url": signed_url}, code

    @require_user_token(PROVIDER)
    def update_uploaded_ts(self, token):
        """
        Fetch the data by reportid from Salvos Table and update \
            the clinician_verified_at column
        param: reportId
        return: uploaded message
        """
        request_data = validate_request()
        report_id = report_id_schema.load(request_data).get("reportId")
        msg, code = self.provider_obj.update_uploaded_ts(report_id)
        return {"message": msg, "status_code": code}, code


    @require_user_token(ADMIN, CUSTOMER_SERVICE, STUDY_MANAGER, PROVIDER)
    def get_providers_list(self, token):
        """
        :param :- page_number, record_per_page, name, external ID
        :return filtered patient list
        """
        request_data = validate_request()
        logging.debug(
            "User: {} with role: {} - is requesting a list of patients".format(token["user_email"],
                                                                               token["user_role"]))
        filter_input = provider_list_schema.load(request_data)
        providers, total = self.provider_obj.get_providers_list(*filter_input)

        return (
            {
                "total": total,
                "page_number": filter_input[0],
                "record_per_page": filter_input[1],
                "data": providers,
                "status_code": http.client.OK,
            },
            http.client.OK,
        )


