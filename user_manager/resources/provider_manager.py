# from flask_restful import Resource
from flask import request, jsonify
from model.user_registration import UserRegister
from model.users import Users
from model.providers import Providers
from utils.common import (
    have_keys,
    encPass)
from utils.jwt import require_user_token
from werkzeug.exceptions import Conflict
from schema.patient_schema import (filter_patient_schema, patient_id_schema)
from utils.constants import ADMIN, PROVIDER
from services.user_services import UserServices
from services.provider_services import ProviderService
from utils.validation import validate_request
from schema.report_schema import report_id_schema
from schema.patient_schema import patient_detail_schema
from schema.report_schema import patient_reports_schema
import http


class provider_manager():
    def __init__(self):
        self.userObj = UserServices()
        self.provider_obj = ProviderService()

    @require_user_token(ADMIN, PROVIDER)
    def register_provider(self, decrypt):
        provider_json = request.get_json()
        if have_keys(
            provider_json,
            'first_name', 'last_name',
            'facility_id', 'phone_number',
            'email', 'password'
                ) is False:
            return {"message": "Invalid Request Parameters"}, 400
        register = (str(provider_json['email']).lower(),
                    provider_json['password'])
        print(register)
        user = (provider_json['first_name'], provider_json['last_name'],
                provider_json['phone_number'])
        facility_id = provider_json["facility_id"]
        self.provider_obj.register_provider(register, user, facility_id)
        return {"message": "Provider Created"}, 201

    @require_user_token(ADMIN, PROVIDER)
    def get_provider_by_id(self, decrypt):
        provider_json = request.get_json()
        if have_keys(provider_json, 'provider_id') is False:
            return {"message": "Invalid Request Parameters"}, 400
        provider_data = Providers.find_by_id(provider_json["provider_id"])
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
        UserRegister.delete_user_by_Userid(user_id=provider_data.user_id)
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
        request_data = validate_request()
        filter_input = filter_patient_schema.load(request_data)
        patients_list, total = self.provider_obj.patients_list(*filter_input)
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
        return {"message": signed_url}, code

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
        print(report_id)
        msg, code = self.provider_obj.update_uploaded_ts(report_id)
        return {"message": msg,
                "status_code": code}, code
