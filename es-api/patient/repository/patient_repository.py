from model.patient import Patient
from model.patients_devices import PatientsDevices
from model.devices import Devices
from db import db
from sqlalchemy.exc import SQLAlchemyError   
from werkzeug.exceptions import InternalServerError, NotFound

class PatientRepository():
    def save_patient(self, user_id, emergency_contact_name, emergency_contact_number, date_of_birth):
        try:
            self.check_user_exist(user_id)
            patient_data = Patient(user_id, emergency_contact_name, emergency_contact_number, date_of_birth)
            Patient.save_patient(patient_data)
            print(patient_data.id)
        except SQLAlchemyError as error:
            db.session.rollback()
            raise InternalServerError(str(error))
    
    def assign_device_to_patient(self,patient_id, device_id):
        try:
            self.check_patient_exist(patient_id)
            self.check_device_exist(device_id)
            patient_device_data = PatientsDevices(patient_id = patient_id, device_id = device_id)
            #PatientsDevices.save_patients_device(patient_device_data)
        except SQLAlchemyError as error:
            db.session.rollback()
            raise InternalServerError(str(error))
        
    def check_patient_exist(self, patient_id):
        try:
            patient = db.session.query(Patient.id).filter_by(id = patient_id).first()
            print("patient", patient)
        except SQLAlchemyError as error:
            raise InternalServerError(str(error))
    
    def check_device_exist(self, device_id):
        print("device_id", device_id)
        device = db.session.query(Devices.id).filter_by(id=device_id).first()
        print(device)
        
    def check_user_exist(self, user_id):
        pass