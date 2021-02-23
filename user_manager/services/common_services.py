from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import InternalServerError, NotFound, Conflict
from model.patient import Patient
from model.devices import Devices
from model.users import Users
from model.user_registration import UserRegister
from db import db


class CommonRepo():
    def __init__(self):
        pass
    
    def check_patient_exist(self, patient_id):
        try:
            exist_patient = db.session.query(Patient). \
                        filter_by(id=patient_id).first()
            if bool(exist_patient) is False:
                raise NotFound('Patient does not exist')
            return exist_patient
        except SQLAlchemyError as error:
            raise InternalServerError(str(error))

   
        
    def is_email_registered(self, email):
        try:
            exist_registration = UserRegister.find_by_email(email)
            if exist_registration is not None:
                raise Conflict(f"email '{email}' already exist")
            return exist_registration
        except SQLAlchemyError as error:
            raise InternalServerError(str(error))

    
