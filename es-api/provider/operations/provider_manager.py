# from flask_restful import Resource
from flask import request
from model.user_registration import UserRegister
from model.users import Users
from model.providers import Providers
from utils.common import (
    have_keys,
    encPass)
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import InternalServerError, Conflict


class provider_manager():
    def __init__(self):
        pass
    
    
    @require_user_token("Admin")
    def register_provider(self, decrypt):
        provider_json = request.get_json()
        if have_keys(
            provider_json,
            'first_name', 'last_name',
            'facility_id', 'phone_number',
            'email', 'password'
                ) is False:
            return {"message": "Invalid Request Parameters"}, 400
        user_exists(provider_json)
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


    @require_user_token("Admin","Provider")
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
    user_reg_data = UserRegister.find_by_username(
        email=provider_json['email']
            )
    if user_reg_data is not None:
        if (Users.find_by_registration_id(
            registration_id=user_reg_data.registration_id
                ) is not None):
            raise Conflict(f'Users Already Register')

    if user_reg_data is not None:
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
            registration_id=user_registration_data.id
            )
        user.save_user()
        user_data = user.find_by_registration_id(user_registration_data.id)
        if user_data is None:
            return {"message": "Server Error"}, 500
        userRole = UserRoles(role_id=3, user_id=user_data.id)
        userRole.save_to_db()
    except SQLAlchemyError as error:
        db.session.rollback()
        raise InternalServerError(str(error))
    return user_data.id
