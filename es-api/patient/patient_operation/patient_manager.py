from flask import jsonify
from werkzeug.exceptions import BadRequest, Conflict
import http
from patient.repository.patient_repository import PatientRepository
from common.common_repo import CommonRepo
from user.repository.user_repository import UserRepository
from model.user_registration import UserRegister
from model.therapy_reports import TherapyReport
from model.authentication_token import AuthenticationToken
from model.salvos import Salvos
from model.user_statuses import UserStatUses
from model.user_status_types import UserStatusType
from utils.validation import validate_request, get_param, validate_number
from utils.jwt import require_user_token
from utils.common import encPass
from patient.schema.patient_schema import (create_patient_schema,
                                           update_patient_schema,
                                           assign_device_schema)
from utils.constants import ADMIN, PROVIDER, PATIENT
from flask import request


class PatientManager():
    def __init__(self):
        self.patientObj = PatientRepository()
        self.userObj = UserRepository()
        self.commonObj = CommonRepo()

    @require_user_token(ADMIN, PROVIDER)
    def create_patient(self, decrypt):
        request_data = validate_request()
        register, user, patient = create_patient_schema.load(request_data)
        self.commonObj.is_email_registered(register[0])
        user_data = UserRegister(email=register[0],
                                 password=encPass(register[1]))
        UserRegister.save_to_db(user_data)
        user_id, user_uuid = self.userObj.save_user(user[0], user[1],
                                                    user[2], user_data.id)
        self.patientObj.save_patient(user_id, patient[0],
                                     patient[1], patient[2])
        self.patientObj.assign_patient_role(user_id)
        return {'message': 'Patient created',
                'data': "user_uuid"}, http.client.CREATED

    @require_user_token(ADMIN, PROVIDER)
    def update_patient(self, decrypt):
        patient_id = request.args.get('id')
        if patient_id is None:
            raise BadRequest("parameter id is missing")
        request_data = validate_request()
        patient = update_patient_schema.load(request_data)
        self.patientObj.update_patient_data(patient_id, patient[0],
                                            patient[1], patient[2])
        return {"message": "Sucessfully updated"}, http.client.OK

    @require_user_token(ADMIN, PROVIDER)
    def delete_patient(self, decrypt):
        patient_id = request.args.get('id')
        if patient_id is None:
            raise BadRequest("parameter id is missing")
        self.patientObj.delete_patient_data(patient_id)
        return {"message": "Patient deleted"}, http.client.OK

    @require_user_token(ADMIN, PROVIDER)
    def assign_device(self, decrypt):
        request_data = validate_request()
        patient_id, device_id = assign_device_schema.load(request_data)
        self.patientObj.assign_device_to_patient(patient_id, device_id)
        print("id", id)
        return {'message': 'Device assigned',
                'statusCode': '201'}, http.client.CREATED

    def patient_device_list(self):
        device_list = self.patientObj.patient_device_list()
        resp = {'devices': device_list}
        return jsonify(resp), http.client.OK

    @require_user_token(PATIENT, ADMIN, PROVIDER)
    def mock_patient_device_list(self, decrypt):
        devices = [['1212', '12EE', True],
                   ['1213', '13EE', True],
                   ['1512', '12TE', False]]
        device_list = [
            {'serial_number': d[0],
             'key': d[1],
             'status': d[2]
             } for d in devices]
        resp = {'devices': device_list}
        return jsonify(resp), http.client.OK
