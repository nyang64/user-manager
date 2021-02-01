from flask import jsonify
from werkzeug.exceptions import BadRequest, Conflict
from datetime import datetime
import http
from patient.repository.patient_repository import PatientRepository
from user.repository.user_repository import UserRepository
from model.user_registration import UserRegister
from utils.validation import validate_request, get_param, validate_number


class PatientManager():
    def __init__(self):
        self.patientObj = PatientRepository()
        self.userObj = UserRepository()

    def create_patient(self):
        request_data = validate_request()
        register, user, patient = self.__read_patient_input(request_data)
        user_data = UserRegister(register[0], register[1], datetime.now())
        exist_user = UserRegister.find_by_username(register[0])
        if exist_user is not None:
            raise Conflict('user already exist')
        UserRegister.save_to_db(user_data)
        user_id = self.userObj.save_user(user[0], user[1], user[2],
                                         user[3], user_data.id)
        patient_id = self.patientObj.save_patient(user_id,
                                                  patient[0],
                                                  patient[1],
                                                  patient[2])
        return {'message': 'patient created',
                'data': patient_id}, http.client.CREATED

    def get_patient(self, id):
        return {"message": "Working on this"}, http.client.CREATED

    def update_patient(self, id):
        return {"message": "Working on this"}, http.client.CREATED

    def delete_patient(self, id):
        return {}, http.client.CREATED

    def assign_device(self, id):
        if id is None:
            raise BadRequest('id is None')
        request_data = validate_request()
        device_id = self.__read_device_input(request_data)
        self.patientObj.assign_device_to_patient(id, device_id)
        print("id", id)
        return {'message': 'Device assigned',
                'statusCode': '201'}, http.client.CREATED

    def patient_device_list(self):
        device_list = self.patientObj.patient_device_list()
        ''' devices = [['1212', '12EE', True],
                   ['1213', '13EE', True],
                   ['1512', '12TE', False]]
        device_list = [
            {'serial_number': d[0],
             'key': d[1],
             'status': d[2]
             } for d in devices] '''
        resp = {'devices': device_list}
        return jsonify(resp), http.client.OK
    
    def mock_patient_device_list(self):
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

    def __read_device_input(self, request_data):
        device_id = int(get_param('device_id', request_data))
        return device_id

    def __read_patient_input(self, request_data):
        # enrolled data question?
        print(request_data)
        username = get_param('username', request_data)
        password = get_param('password', request_data)
        first_name = get_param('first_name', request_data)
        last_name = get_param('last_name', request_data)
        phone_number = get_param('phone_number', request_data)
        emergency_contact_name = get_param('emergency_contact_name',
                                           request_data)
        emergency_contact_number = get_param('emergency_contact_number',
                                             request_data)
        date_of_birth = get_param('date_of_birth',
                                  request_data)
        validate_number(phone_number)
        validate_number(emergency_contact_number)
        register = (username, password)
        user = (first_name, last_name, phone_number, username)
        patient = (emergency_contact_name,
                   emergency_contact_number, date_of_birth)
        return register, user, patient
