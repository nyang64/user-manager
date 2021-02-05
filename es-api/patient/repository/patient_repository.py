from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import InternalServerError
from model.patient import Patient
from model.patients_devices import PatientsDevices
from model.devices import Devices
from model.user_roles import UserRoles
from common.common_repo import CommonRepo
from db import db


class PatientRepository():
    def __init__(self):
        self.commonObj = CommonRepo()
        
    def save_patient(self, user_id, emer_contact_name,
                     emer_contact_no, date_of_birth):
        try:
            self.commonObj.check_user_exist(user_id)
            patient_data = Patient(user_id=user_id,
                                   emergency_contact_name=emer_contact_name,
                                   emergency_contact_number=emer_contact_no,
                                   date_of_birth=date_of_birth)
            Patient.save_patient(patient_data)
            print(patient_data.id)
            if patient_data.id is None:
                raise SQLAlchemyError('error while adding patient')
            return patient_data.id
        except SQLAlchemyError as error:
            db.session.rollback()
            raise InternalServerError(str(error))

    def assign_device_to_patient(self, patient_id, device_id):
        try:
            self.commonObj.check_patient_exist(patient_id)
            self.commonObj.check_device_exist(device_id)
            patient_device_data = PatientsDevices(patient_id=patient_id,
                                                  device_id=device_id)
            PatientsDevices.save_db(patient_device_data)
        except SQLAlchemyError as error:
            db.session.rollback()
            raise InternalServerError(str(error))

    def patient_device_list(self):
        device_list = db.session.query(Devices).join(PatientsDevices). \
            filter(Devices.id == PatientsDevices.device_id). \
            join(Patient).filter(
                Patient.id == PatientsDevices.patient_id).all()
        json_device = [{'serial_number': d.serial_number,
                        'key': d.encryption_key,
                        'status': d.status}
                       for d in device_list]
        print(json_device)
        return json_device

    def update_patient_data(self, id, emer_contact_name,
                            emer_contact_no, dob):
        exist_patient = self.commonObj.check_patient_exist(id)
        exist_patient.emergency_contact_name = emer_contact_name
        exist_patient.emergency_contact_number = emer_contact_no
        exist_patient.date_of_birth = dob
        Patient.update_db(exist_patient)

    def delete_patient_data(self, id):
        exist_patient = self.commonObj.check_patient_exist(id)
        Patient.delete_obj(exist_patient)
        
    def assign_patient_role(self, user_id):
        try:
            self.commonObj.check_user_exist(user_id)
            user_role = UserRoles(role_id=3, user_id=user_id)
            UserRoles.save_db(user_role)
            if user_role.id is None:
                raise SQLAlchemyError('Roles not updated')
        except SQLAlchemyError as error:
            raise InternalServerError(str(error))
