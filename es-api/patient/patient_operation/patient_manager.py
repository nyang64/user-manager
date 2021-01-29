from flask import jsonify
from werkzeug.exceptions import BadRequest
import http
from patient.repository.patient_repository import PatientRepository
from utils.validation import validate_request, get_param, validate_number


class PatientManager():
    def __init__(self):
        self.patientObj = PatientRepository()

    def create_patient(self, id):
        request_data = validate_request()
        emergency_contact_name, emergency_contact_number, date_of_birth = self.__read_patient_input(request_data)
        patient_id = self.patientObj.save_patient(id, emergency_contact_name,
                                                  emergency_contact_number,
                                                  date_of_birth)
        return {'message': 'patient created',
                'data': patient_id}, http.client.CREATED

    def get_patient(self, id):
        return {}, http.client.CREATED

    def update_patient(self, id):
        return {}, http.client.CREATED

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
        emergency_contact_name = get_param('emergency_contact_name',
                                           request_data)
        emergency_contact_number = get_param('emergency_contact_number',
                                             request_data)
        date_of_birth = get_param('date_of_birth',
                                  request_data)
        validate_number(emergency_contact_number)
        return emergency_contact_name, emergency_contact_number, date_of_birth
    