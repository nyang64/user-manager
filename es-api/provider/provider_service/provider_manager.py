from flask_restful import Resource
from flask import request
from model.user_registration import UserRegister
from model.user import User
from model.user_otp import UserOTPModel
from model.es_users import ES_Users
from model.address import Address
from model.devices import Devices
from model.patient import Patient
from model.providers import Providers
from database.user import UserSchema
from utils.common import(
    have_keys,
    tokenTime,
    generateOTP,
    MyEncoder,
    encPass)
from utils.jwt import require_user_token, require_refresh_token
import datetime
import jwt
import bcrypt

class provider_manager():
    def __init__(self):
        pass

# first_name, lASt_name, facility_id, phONe, email, scope_id, user_id

    def register_provider(self):
        provider_json = request.get_json()
        if have_keys(
            provider_json,
            'first_name', 'last_name',
            'facility_id', 'phone_number',
            'username', 'password'
                ) is False:
            return {"message": "Invalid Request Parameters"}, 400
        if (UserRegister.find_by_username(
            username=provider_json['username']
                ) is not None):
            return {"message": "User Already Register"}, 400
        if (User.find_by_email(
            email=provider_json['username']
                ) is not None):
            return {"message": "User Already Exist"}, 400
        usrReg = UserRegister(
            username=provider_json['username'],
            password=encPass(provider_json['password']),
            created_at=datetime.datetime.now()
            )
        usrReg.save_to_db()
        usrRegDt = UserRegister.find_by_username(
            username=provider_json['username']
            )
        if usrRegDt is None:
            return {"message": "Server Error"}, 500
        usr = User(
            first_name=provider_json['first_name'],
            last_name=provider_json['last_name'],
            phone_number=provider_json['phone_number'],
            email=provider_json['username'],
            registration_id=usrReg.id
            )
        usr.save_user()
        usrDt = usr.find_by_email(provider_json['username'])
        if usrDt is None:
            return {"message": "Server Error"}, 500
        prov = Providers(
            user_id=usrDt.id,
            facility_id=provider_json["facility_id"],
            created_at=datetime.datetime.now()
            )
        prov.save_to_db()
        return {"message": "Provider Created"}, 201

    def get_provider_by_id(self):
        provider_json = request.get_json()
        if have_keys(provider_json, 'provider_id') is False:
            return {"message": "Invalid Request Parameters"}, 400
        udt = Providers.find_by_id(provider_json["provider_id"])
        if udt is None:
            return {"message": "No Such Provider Exist"}, 404
        print("provider", udt)
        dta = udt.__dict__
        del dta['_sa_instance_state']
        return {
            "message": "User Found",
            "Data": [dta]
            }, 200
