from flask import jsonify, request
from werkzeug.exceptions import BadRequest
import http
from services.patient_services import PatientServices
from utils.validation import validate_request
from utils.jwt import require_user_token
from schema.patient_schema import (create_patient_schema,
                                   update_patient_schema,
                                   assign_device_schema,)
from utils.constants import ADMIN, PROVIDER, PATIENT


class PatientManager():
    def __init__(self):
        self.patient_obj = PatientServices()
        
    def create(self):
        request_data = validate_request()
        cr = create_patient_schema.load(request_data)
        print(cr)
        return {}

    @require_user_token(ADMIN, PROVIDER)
    def create_patient(self, decrypt):
        request_data = validate_request()
        register, user, patient = create_patient_schema.load(request_data)
        user_id, user_uuid = self.patient_obj.register_patient(register,
                                                               user, patient)
        return {'message': 'Patient created',
                'data': {
                    'patient_uuid': user_uuid,
                    'patient_id': user_id
                    },
                'status_code': '201'}, http.client.CREATED

    @require_user_token(ADMIN, PROVIDER)
    def update_patient(self, decrypt):
        patient_id = request.args.get('id')
        if patient_id is None:
            raise BadRequest("parameter id is missing")
        request_data = validate_request()
        patient = update_patient_schema.load(request_data)
        self.patient_obj.update_patient_data(patient_id, patient[0],
                                             patient[1], patient[2])
        return {"message": "Sucessfully updated"}, http.client.OK

    @require_user_token(ADMIN, PROVIDER)
    def delete_patient(self, decrypt):
        patient_id = request.args.get('id')
        if patient_id is None:
            raise BadRequest("parameter id is missing")
        self.patient_obj.delete_patient_data(patient_id)
        return {"message": "Patient deleted"}, http.client.OK

    @require_user_token(ADMIN, PROVIDER)
    def assign_device(self, decrypt):
        request_data = validate_request()
        patient_id, device_id = assign_device_schema.load(request_data)
        self.patient_obj.assign_device_to_patient(patient_id, device_id)
        print("id", id)
        return {'message': 'Device assigned',
                'status_code': '201'}, http.client.CREATED

    def patient_device_list(self):
        device_list = self.patient_obj.patient_device_list()
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
