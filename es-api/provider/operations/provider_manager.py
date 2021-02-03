from flask_restful import Resource
from flask import request
from model.user_registration import UserRegister
from model.users import Users
from model.user_otp import UserOTPModel
from model.address import Address
from model.devices import Devices
from model.patient import Patient
from model.providers import Providers
from model.authentication_token import AuthenticationToken
from model.device_status_types import DeviceStatusType
from model.device_statuses import DeviceStatUses
from model.facilities import Facilities
from model.roles import Roles
from model.salvos import Salvos
from model.therapy_reports import TherapyReport
from model.user_roles import UserRoles
from model.user_status_types import UserStatusType
from model.user_statuses import UserStatUses
from database.user import UserSchema
from utils.common import (
    have_keys,
    tokenTime,
    generateOTP,
    MyEncoder,
    encPass)
from utils.jwt import require_user_token, require_refresh_token
import datetime
import jwt
import bcrypt
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import InternalServerError, NotFound, Conflict


class provider_manager():
    def __init__(self):
        pass

    def register_provider(self):
        provider_json = request.get_json()
        if have_keys(
            provider_json,
            'first_name', 'last_name',
            'facility_id', 'phone_number',
            'email', 'password'
                ) is False:
            return {"message": "Invalid Request Parameters"}, 400
        user_id = insert_ref(provider_json)
        provider = Providers(
            user_id=user_id,
            facility_id=provider_json["facility_id"]
            )
        try:
            provider.save_to_db()
        except SQLAlchemyError as error:
            db.session.rollback()
            raise InternalServerError(str(error)) 
        return {"message": "Provider Created"}, 201

    def get_provider_by_id(self):
        provider_json = request.get_json()
        if have_keys(provider_json, 'provider_id') is False:
            return {"message": "Invalid Request Parameters"}, 400
        provider_data = Providers.find_by_id(provider_json["provider_id"])
        if provider_data is None:
            return {"message": "No Such Provider Exist"}, 404
        provider_data_json = provider_data.__dict__
        del provider_data_json['_sa_instance_state']
        return {
            "message": "Users Found",
            "Data": [provider_data_json]
            }, 200


def user_exists(provider_json):
    if (UserRegister.find_by_username(
        email=provider_json['email']
            ) is not None):
        raise Conflict(f'Users Already Register')
    if (Users.find_by_email(
        email=provider_json['email']
            ) is not None):
        raise Conflict(f'Users Already Register')


def insert_ref(provider_json):
    try:
        user_registration = UserRegister(
            email=provider_json['email'],
            password=encPass(provider_json['password']),
            )
        user_registration.save_to_db()
        user_registration_data = UserRegister.find_by_username(
            email=provider_json['email']
            )
        if user_registration_data is None:
            return {"message": "Server Error"}, 500
        user = Users(
            first_name=provider_json['first_name'],
            last_name=provider_json['last_name'],
            phone_number=provider_json['phone_number'],
            email=provider_json['email'],
            registration_id=user_registration_data.id
            )
        user.save_user()
        user_data = user.find_by_email(provider_json['email'])
        if user_data is None:
            return {"message": "Server Error"}, 500
        userRole = UserRoles(role_id=3, user_id=user_data.id)
        userRole.save_to_db()
    except SQLAlchemyError as error:
        db.session.rollback()
        raise InternalServerError(str(error))
    return user_data.id
