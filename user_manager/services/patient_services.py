from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import InternalServerError, NotFound
from model.patient import Patient
from model.patients_devices import PatientsDevices
from model.users import Users
from model.user_registration import UserRegister
from db import db
from services.user_services import UserServices
from services.auth_services import AuthServices
from services.repository.db_repositories import DbRepository
from utils.constants import GET_DEVICE_DETAIL_URL, CHECK_DEVICE_EXIST_URL
import requests


class PatientServices(DbRepository):
    def __init__(self):
        self.auth_obj = AuthServices()
        self.user_obj = UserServices()

    def register_patient(self, register, user, patient):
        from utils.constants import PATIENT
        reg_id = self.auth_obj.register_new_user(register[0],
                                                 register[1])
        user_id, user_uuid = self.user_obj.save_user(user[0], user[1],
                                                     user[2], reg_id)
        self.save_patient(user_id, patient[0],
                          patient[1], patient[2])
        self.user_obj.assign_role(user_id, PATIENT)
        self.commit_db()
        return user_id, user_uuid

    def save_patient(self, user_id, emer_contact_name,
                     emer_contact_no, date_of_birth):
        try:
            Users.check_user_exist(user_id)
            patient_data = Patient(user_id=user_id,
                                   emergency_contact_name=emer_contact_name,
                                   emergency_contact_number=emer_contact_no,
                                   date_of_birth=date_of_birth)
            self.flush_db(patient_data)
            if patient_data.id is None:
                raise SQLAlchemyError('error while adding patient')
            return patient_data.id
        except SQLAlchemyError as error:
            raise InternalServerError(str(error))

    def assign_device_to_patient(self, patient_device):
        exist_patient = Patient.check_patient_exist(patient_device.patient_id)
        payload = {'serial_number':patient_device.device_id}
        r = requests.get(CHECK_DEVICE_EXIST_URL, params=payload)
        if int(r.status_code) == 404:
            MSG = f'Device serial number {patient_device.device_id} not found'
            raise NotFound(MSG)
        if bool(exist_patient) is False:
            raise NotFound('patient record not found')
        try:
            self.save_db(patient_device)
            if patient_device.id is None:
                raise SQLAlchemyError('Failed to assign device')
        except SQLAlchemyError as error:
            raise InternalServerError(str(error))

    def patient_device_list(self, token):
        from utils.common import rename_keys
        import json
        device_serial_numbers = db.session.query(UserRegister, Users)\
            .join(Users, UserRegister.id == Users.registration_id)\
            .join(Patient, Users.id == Patient.user_id)\
            .join(PatientsDevices, Patient.id == PatientsDevices.patient_id)\
            .filter(UserRegister.email == token.get('user_email'))\
            .with_entities(PatientsDevices.device_id)\
            .all()
        print(device_serial_numbers)
        # Count should be same as the original one
        new_keys = {'encryption_key': 'key', 'serial_number': 'serial_number'}
        devices = []
        for d in device_serial_numbers:
            payload = {'serial_number': str(d[0])}
            r = requests.get(GET_DEVICE_DETAIL_URL,
                             params=payload)
            if r.status_code == 200:
                response = json.loads(r.text)
                device = response['data'] if 'data' in response else None
                try:
                    device_info = rename_keys(device, new_keys)
                except AttributeError:
                    device_info = {}
                devices.append(device_info)
        return devices

    def update_patient_data(self, patient_id, emer_contact_name,
                            emer_contact_no, dob):
        exist_patient = Patient.check_patient_exist(patient_id)
        if bool(exist_patient) is False:
            raise NotFound('patient record not found')
        exist_patient.emergency_contact_name = emer_contact_name
        exist_patient.emergency_contact_number = emer_contact_no
        exist_patient.date_of_birth = dob
        Patient.update_db(exist_patient)

    def delete_patient_data(self, patient_id):
        exist_patient = Patient.check_patient_exist(patient_id)
        if bool(exist_patient) is False:
            raise NotFound('patient record not found')
        self.user_obj.delete_user_byid(exist_patient.user_id)
