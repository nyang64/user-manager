from sqlalchemy.exc import SQLAlchemyError, ProgrammingError
from werkzeug.exceptions import (InternalServerError, NotFound,
                                 Conflict, NotAcceptable)
from model.patient import Patient
from model.patients_devices import PatientsDevices
from model.users import Users
from model.user_registration import UserRegister
from db import db
from services.user_services import UserServices
from services.auth_services import AuthServices
from services.repository.db_repositories import DbRepository
from schema.patients_providers_schema import PatientsProvidersSchema
from utils.constants import (GET_DEVICE_DETAIL_URL,
                             CHECK_DEVICE_EXIST_URL,
                             UPDATE_DEVICE_STATUS_URL,
                             GET_DEVICE_STATUS_URL,
                             DEVICE_STATUS,
                             LOGIN_URL)
import requests
import logging


class PatientServices(DbRepository):
    def __init__(self):
        self.auth_obj = AuthServices()
        self.user_obj = UserServices()

    def register_patient(self, register, user, patient,
                         outpatient_id, prescribing_id):
        from utils.constants import PATIENT
        reg_id = self.auth_obj.register_new_user(register[0],
                                                 register[1])
        user_id, user_uuid = self.user_obj.save_user(user[0], user[1],
                                                     user[2], reg_id)
        patient_id = self.save_patient(user_id, patient[0], patient[1],
                                       patient[2], patient[3], patient[4])
        self.user_obj.assign_role(user_id, PATIENT)
        # create PatientProvider
        patient_provider_schema = PatientsProvidersSchema()
        out_patient_provider = patient_provider_schema.load({
            "patient_id": patient_id,
            "provider_id": outpatient_id,
            "provider_role_id": 2
        })
        out_patient_provider.save_to_db()
        pre_patient_provider = patient_provider_schema.load({
            "patient_id": patient_id,
            "provider_id": prescribing_id,
            "provider_role_id": 1
        })
        pre_patient_provider.save_to_db()

        self.commit_db()
        return user_id, user_uuid, patient_id

    def save_patient(self, user_id, emer_contact_name,
                     emer_contact_no, date_of_birth, gender, provider_id):
        try:
            Users.check_user_exist(user_id)
            patient_data = Patient(user_id=user_id,
                                   gender=gender,
                                   emergency_contact_name=emer_contact_name,
                                   emergency_contact_number=emer_contact_no,
                                   date_of_birth=date_of_birth,
                                   provider_id=provider_id)
            self.flush_db(patient_data)
            if patient_data.id is None:
                raise SQLAlchemyError('error while adding patient')
            return patient_data.id
        except SQLAlchemyError as error:
            logging.error(error)
            raise InternalServerError(str(error))

    def count_device_assigned(self, patient_id):
        import json
        auth_token = self.get_auth_token()
        header = {'Authorization': auth_token}
        try:
            # Get the Device Assigned Detail
            # Hit Check Device Status
            # If device found status is in assigned count 2 then raise error
            logging.info('Fetching List of Device Assigned to patient')
            devices = db.session.query(PatientsDevices.device_serial_number)\
                .filter(PatientsDevices.patient_id == patient_id).all()
            if len(devices) < 2:
                return False
            logging.info('Checking the Device Status')
            assigned_count = 0
            for device in devices:
                payload = {'serial_number': device[0]}
                logging.info('Request Payload {}'.format(payload))
                resp = requests.get(GET_DEVICE_STATUS_URL,
                                    headers=header,
                                    params=payload)
                logging.info('Request finished with status code {}'.format(
                    resp.status_code))
                logging.info('Headers value {}'.format(resp.headers))
                logging.info('response {}'.format(resp.text))
                status = json.loads(resp.text).get('data')
                logging.info('Device Status {}'.format(status))
                logging.info('The Called API {}'.format(resp.url))
                if 'assigned' in str(status).lower():
                    assigned_count += 1
            if assigned_count >= 2:
                logging.warning('2 Device is already assigned')
                raise NotAcceptable('2 Devices is already assigned.')
        except (ProgrammingError, SQLAlchemyError) as error:
            raise InternalServerError(str(error))

    def check_device_assigned(self, device_serial_number):
        is_assign = PatientsDevices.check_device_assigned(
            device_serial_number)
        print('Device Assigned to patient' + str(is_assign))
        logging.debug('Device Assigned to patient : {}'.format(
            bool(is_assign)))
        if bool(is_assign) is True:
            logging.warning(
                'Device {} Already assigned to patient'.format(
                    device_serial_number))
            raise Conflict('Device Already assigned to patient')

    def check_device_number_exist(self, device_serial_number):
        auth_token = self.get_auth_token()
        header = {'Authorization': auth_token}
        payload = {'serial_number': device_serial_number}
        logging.info('Request payload {}'.format(payload))
        print(CHECK_DEVICE_EXIST_URL)
        r = requests.get(CHECK_DEVICE_EXIST_URL,
                         headers=header,
                         params=payload)
        print("....." + r)
        logging.debug('Request finished with status code {}'.format(
            r.status_code))
        logging.debug('response {}'.format(r.text))
        logging.debug('The Called API {}'.format(r.url))
        if int(r.status_code) == 404:
            MSG = 'Device serial number {} not found'.format(
                device_serial_number)
            raise NotFound(MSG)

    def update_device_status(self, device_serial_number):
        auth_token = self.get_auth_token()
        header = {'Authorization': auth_token}
        logging.info('Updating the device status')
        payload = {'serial_number': device_serial_number,
                   'name': DEVICE_STATUS}
        logging.info('Request payload {}'.format(payload))
        resp = requests.post(UPDATE_DEVICE_STATUS_URL,
                             headers=header,
                             json=payload)
        logging.info('Request finished with status code {}'.format(
            resp.status_code))
        logging.info('response {}'.format(resp.text))
        logging.info('The Called API {}'.format(resp.url))
        if int(resp.status_code) != 201:
            logging.warning('Failed to update the device status')
            raise InternalServerError(
                'Failed to update status. Device Not Assigned')
        else:
            return True

    def assign_device_to_patient(self, patient_device):
        logging.debug('Assign to device patient started')
        print('Assign to device patient started')
        exist_patient = Patient.find_by_id(patient_device.patient_id)
        if bool(exist_patient) is False:
            logging.warning('Patient Record Not Found')
            raise NotFound('patient record not found')
        self.check_device_assigned(patient_device.device_serial_number)
        self.count_device_assigned(patient_device.patient_id)
        # Calling device API
        self.check_device_number_exist(patient_device.device_serial_number)
        try:
            logging.info('Saving to the database')
            self.flush_db(patient_device)
            if patient_device.id is None:
                logging.warning('Failed to save device to database')
                raise SQLAlchemyError('Failed to assign device')
            logging.info('Assigned Device')
            # Updating device status
            updated = self.update_device_status(
                patient_device.device_serial_number)
            if updated is True:
                self.commit_db()
        except SQLAlchemyError as error:
            logging.error(
                'Error Occured while assign device to patient {}'.format(
                    str(error)))
            raise InternalServerError(str(error))

    def patient_device_list(self, token):
        from utils.common import rename_keys
        import json
        auth_token = self.get_auth_token()
        header = {'Authorization': auth_token}
        print("In Patient Device list of patient services")
        device_serial_numbers = db.session.query(UserRegister, Users)\
            .join(Users, UserRegister.id == Users.registration_id)\
            .join(Patient, Users.id == Patient.user_id)\
            .join(PatientsDevices, Patient.id == PatientsDevices.patient_id)\
            .filter(UserRegister.email == token.get('user_email'))\
            .with_entities(PatientsDevices.device_serial_number)\
            .all()
        # Count should be same as the original one
        new_keys = {'encryption_key': 'key', 'serial_number': 'serial_number'}
        devices = []
        for d in device_serial_numbers:
            print('Fetching the device detail')
            payload = {'serial_number': str(d[0])}
            print('API calling', GET_DEVICE_DETAIL_URL)
            print('payload', payload)
            r = requests.get(GET_DEVICE_DETAIL_URL,
                             headers=header,
                             params=payload)
            print('Request finished', r.status_code)
            print('response', r.text)
            print('The URL fetch detail', r.url)
            if r.status_code == 200:
                response = json.loads(r.text)
                print('API response', response)
                device = response['data'] if 'data' in response else None
                try:
                    device_info = rename_keys(device, new_keys)
                except AttributeError as e:
                    logging.error(e)
                    device_info = {}
                devices.append(device_info)
        return devices

    def update_patient_data(self, patient_id, emer_contact_name,
                            emer_contact_no, dob):
        exist_patient = Patient.find_by_id(patient_id)
        if bool(exist_patient) is False:
            raise NotFound('patient record not found')
        exist_patient.emergency_contact_name = emer_contact_name
        exist_patient.emergency_contact_number = emer_contact_no
        exist_patient.date_of_birth = dob
        self.update_db(exist_patient)

    def delete_patient_data(self, patient_id):
        exist_patient = Patient.find_by_id(patient_id)
        if bool(exist_patient) is False:
            raise NotFound('patient record not found')
        self.user_obj.delete_user_byid(exist_patient.user_id)

    def get_auth_token(self):
        import json
        import os
        from config import read_environ_value
        value = os.environ.get('SECRET_MANAGER_ARN')
        DEVICE_EMAIL = read_environ_value(value, 'DEVICE_EMAIL')
        DEVICE_PASSWORD = read_environ_value(value, 'DEVICE_PASSWORD')
        DEVICE_EMAIL = "deviceadmin@elementsci.com"
        DEVICE_PASSWORD = "device12345"
        data = {"email": DEVICE_EMAIL, "password": DEVICE_PASSWORD}
        resp = requests.post(LOGIN_URL, json=data)
        if resp.status_code == 200:
            return json.loads(resp.text).get('id_token')
        else:
            return None
