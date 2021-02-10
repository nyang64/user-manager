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

    def check_device_exist(self, device_id):
        try:
            exist_device = db.session.query(Devices)\
                .filter_by(id=device_id).first()
            if bool(exist_device) is False:
                raise NotFound('device does not exist')
            return exist_device
        except SQLAlchemyError as error:
            raise InternalServerError(str(error))

    def check_user_exist(self, user_id):
        try:
            exist_user = db.session.query(Users)\
                .filter_by(id=user_id).first()
            if bool(exist_user) is False:
                raise NotFound('user does not exist')
            return exist_user
        except SQLAlchemyError as error:
            raise InternalServerError(str(error))
        
    def is_email_registered(self, email):
        try:
            exist_registration = UserRegister.find_by_username(email)
            if exist_registration is not None:
                raise Conflict(f"email '{email}' already exist")
            return exist_registration
        except SQLAlchemyError as error:
            raise InternalServerError(str(error))

    def get_detail_by_email(self, email):
        ''' Get the detail of logged in user by email id'''
        try:
            exist_registration = UserRegister.find_by_username(email)
            if exist_registration is None:
                raise NotFound(f'{email} not found')
            user = db.session.query(Users.id, Users.uuid, UserRegister.id)\
                .filter(UserRegister.id == Users.registration_id)\
                .filter(UserRegister.email == email).first()
            if user is None:
                raise NotFound('user detail not found')
            return user
        except SQLAlchemyError as error:
            raise InternalServerError(str(error))
