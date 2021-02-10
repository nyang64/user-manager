from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import InternalServerError
from model.patients_devices import PatientsDevices
from model.patient import Patient
from model.user_roles import UserRoles
from user.repository.user_repository import UserRepository
from authentication.repository.auth_repo import AuthRepository
from common.common_repo import CommonRepo



class PatientRepository():
    def __init__(self):
        self.common_obj = CommonRepo()
        self.auth_obj = AuthRepository()
        self.user_obj = UserRepository()

    def add_patient(self, register, user, patient):
        reg_id = self.auth_obj.register_user(register[0],
                                             register[1])
        user_id, user_uuid = self.user_obj.save_user(user[0], user[1],
                                                     user[2], reg_id)
        self.save_patient(user_id, patient[0],
                          patient[1], patient[2])
        self.assign_patient_role(user_id)
        Patient.commit_db(self)
        return user_id, user_uuid

    def save_patient(self, user_id, emer_contact_name,
                     emer_contact_no, date_of_birth):
        try:
            self.common_obj.check_user_exist(user_id)
            patient_data = Patient(user_id=user_id,
                                   emergency_contact_name=emer_contact_name,
                                   emergency_contact_number=emer_contact_no,
                                   date_of_birth=date_of_birth)
            Patient.flush_db(patient_data)
            if patient_data.id is None:
                raise SQLAlchemyError('error while adding patient')
            return patient_data.id
        except SQLAlchemyError as error:
            raise InternalServerError(str(error))

    def assign_device_to_patient(self, patient_id, device_id):
        try:
            self.common_obj.check_patient_exist(patient_id)
            self.common_obj.check_device_exist(device_id)
            patient_device_data = PatientsDevices(patient_id=patient_id,
                                                  device_id=device_id)
            PatientsDevices.flush_db(patient_device_data)
            PatientsDevices.commit_db(self)
        except SQLAlchemyError as error:
            raise InternalServerError(str(error))

    def patient_device_list(self):
        json_device = {'serial_number': "working"}
        return json_device

    def update_patient_data(self, id, emer_contact_name,
                            emer_contact_no, dob):
        exist_patient = self.common_obj.check_patient_exist(id)
        exist_patient.emergency_contact_name = emer_contact_name
        exist_patient.emergency_contact_number = emer_contact_no
        exist_patient.date_of_birth = dob
        Patient.update_db(exist_patient)

    def delete_patient_data(self, id):
        exist_patient = self.common_obj.check_patient_exist(id)
        Patient.delete_obj(exist_patient)

    def assign_patient_role(self, user_id):
        try:
            self.common_obj.check_user_exist(user_id)
            user_role = UserRoles(role_id=3, user_id=user_id)
            UserRoles.flush_db(user_role)
            if user_role.id is None:
                raise SQLAlchemyError('Roles not updated')
        except SQLAlchemyError as error:
            raise InternalServerError(str(error))
