from flask import request, jsonify
from utils.common import have_keys
import http
import logging

from utils.jwt import require_user_token
from utils.constants import ADMIN, PROVIDER
from utils.validation import validate_request

from model.users import Users
from model.providers import Providers
from model.facilities import Facilities
from model.address import Address
from model.providers_roles import ProviderRoles
from model.user_registration import UserRegister

from services.user_services import UserServices
from services.provider_services import ProviderService

from schema.address_schema import AddressSchema
from schema.report_schema import report_id_schema
from schema.patient_schema import (patient_detail_schema, filter_patient_schema, patient_id_schema)
from schema.report_schema import patient_reports_schema
from schema.providers_schema import ProvidersSchema
from schema.providers_roles_schema import ProvidersRolesSchema
from schema.user_schema import UserSchema
from schema.register_schema import RegistrationSchema

provider_schema = ProvidersSchema()
providers_schema = ProvidersSchema(many=True)
providers_roles_schema = ProvidersRolesSchema(many=True)
address_schema = AddressSchema()
register_schema = RegistrationSchema()
user_schema = UserSchema()

class provider_manager():
    def __init__(self):
        self.userObj = UserServices()
        self.provider_obj = ProviderService()

    @require_user_token(ADMIN, PROVIDER)
    def register_provider(self, device):
        provider_json = request.get_json()

        if have_keys(
            provider_json,
            'first_name', 'last_name',
            'facility_id', 'phone_number',
            'email', 'password', 'role'
                ) is False:
            return {"message": "Invalid Request Parameters"}, 400

        register = (str(provider_json['email']).lower(),
                    provider_json['password'])
        user = (provider_json['first_name'], provider_json['last_name'],
                provider_json['phone_number'])

        facility_id = provider_json["facility_id"]
        role_name = provider_json["role"]
        provider_id = self.provider_obj.register_provider_service(register, user, facility_id, role_name)

        provider = Providers.find_by_id(provider_id)
        facility = Facilities.find_by_id(int(facility_id))
        address = Address.find_by_id(facility.address_id)
        provider_roles = ProviderRoles.find_by_provider_id(provider_id)
        user = Users.find_by_id(provider.user_id)
        registration = UserRegister.find_by_id(user.registration_id)

        response = {
            "registration": register_schema.dump(registration),
            "user": user_schema.dump(user),
            "provider_role": providers_roles_schema.dump(provider_roles),
            "facility": {
                "name": facility.name,
                "address": address_schema.dump(address),
                "on_call_phone": facility.on_call_phone
            }
        }
        response.update(provider_schema.dump(provider))

        return response, 201

    @require_user_token(ADMIN, PROVIDER)
    def get_provider_by_id(self, decrypt):
        provider_id = request.args.get('provider_id')
        provider_data = Providers.find_by_id(provider_id)
        if provider_data is None:
            return {"message": "No Such Provider Exist"}, 404
        provider_data_json = provider_data.__dict__
        del provider_data_json['_sa_instance_state']
        return {
            "message": "Users Found",
            "Data": [provider_data_json]
            }, 200

    @require_user_token(ADMIN)
    def get_providers(self, decrypt):
        provider_data = Providers.find_providers()
        if provider_data is None or provider_data == []:
            return {"message": "No Providers Found"}, 404
        providers_data = [
            {
                'id': user.id,
                'user_id': user.user_id,
                'facility_id': user.facility_id
            }for user in provider_data]
        return {
            "message": "Users Found",
            "Data": providers_data
            }, 200

    @require_user_token(ADMIN)
    def delete_provider(self, decrypt):
        provider_json = request.get_json()
        if have_keys(provider_json, 'provider_id') is False:
            return {"message": "Invalid Request Parameters"}, 400
        provider_data = Providers.find_by_id(id=provider_json["provider_id"])
        if provider_data is None:
            return {"message": "Unable To Delete, No Such Provider Exist"}, 404
        self.userObj.delete_user_byid(provider_data.user_id)
        return {"message": "Provider Deleted"}, 200

    @require_user_token(ADMIN, PROVIDER)
    def update_provider(self, decrypt):
        provider_json = request.get_json()
        if have_keys(
                provider_json,
                'provider_id',
                'first_name',
                'last_name',
                'phone_number') is False:
            return {"message": "Invalid Request Parameters"}, 400
        provider_data = Providers.find_by_id(id=provider_json["provider_id"])
        if provider_data is None:
            return {"message": "No Such Provider Exist"}, 404
        self.userObj.update_user_byid(
            provider_data.user_id,
            provider_json["first_name"],
            provider_json["last_name"],
            provider_json["phone_number"]
        )
        return {"message": "Provider Updated"}, 200

    @require_user_token(PROVIDER)
    def get_patient_list(self, token):
        '''
        :param :- page_number, record_per_page, first_name,
                  last_name, date_of_birth, report_id
        :return filtered patient list
        '''

        provider = Providers.find_by_email(token['user_email'])
        request_data = validate_request()
        filter_input = filter_patient_schema.load(request_data)
        patients_list, total = self.provider_obj.patients_list(provider.id, *filter_input)

        return {"total": total,
                "page_number": filter_input[0],
                "record_per_page": filter_input[1],
                "data": patients_list,
                "status_code": http.client.OK}, http.client.OK

    @require_user_token(PROVIDER)
    def get_patient_detail_byid(self, token):
        '''
        Fetch the patient detail by their patientid
        param: patientID
        return: patient detail in dict format
        '''
        request_data = request.args
        provider = Providers.find_by_email(token['user_email'])
        patient_id = patient_id_schema.load(request_data).get('patientID')
        patient_data, reports = self.provider_obj.patient_detail_byid(
            patient_id)
        patient_data = patient_detail_schema.dump(patient_data)
        patient_data['report'] = patient_reports_schema.dump(reports)
        return jsonify(patient_data), http.client.OK

    @require_user_token(PROVIDER)
    def get_report_signed_link(self, token):
        '''
        Fetch the key by reportid from Salvos Table and get the signed url
        param: reportId
        return: Report Signed URL
        '''
        request_data = request.args
        report_id = report_id_schema.load(request_data).get('reportId')
        signed_url, code = self.provider_obj.report_signed_link(report_id)
        return {"report_url": signed_url}, code

    @require_user_token(PROVIDER)
    def update_uploaded_ts(self, token):
        '''
        Fetch the data by reportid from Salvos Table and update \
            the clinician_verified_at column
        param: reportId
        return: uploaded message
        '''
        request_data = validate_request()
        report_id = report_id_schema.load(request_data).get('reportId')
        msg, code = self.provider_obj.update_uploaded_ts(report_id)
        return {"message": msg,
                "status_code": code}, code

    @require_user_token(ADMIN)
    def add_facility(self, decrypt):
        ''' Add address, Facility and assign address id to facility table '''
        from schema.facility_schema import add_facility_schema
        from services.facility_services import FacilityService
        logging.info('Request Received to add facility')
        request_data = validate_request()
        address, facility_name = add_facility_schema.load(request_data)
        logging.info('Facility Name: {}'.format(facility_name))
        logging.info('Address Info: {}'.format(address))
        facility_obj = FacilityService()
        aid, fid = facility_obj.register_facility(address, facility_name)
        return {'address_id': aid,
                'facility_id': fid,
                'status_code': http.client.CREATED}, http.client.CREATED
