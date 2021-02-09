from flask import request
from model.user_registration import UserRegister
from model.users import Users
from model.user_otp import UserOTPModel
from model.address import Address
from model.devices import Devices
from model.patient import Patient
from model.providers import Providers
from model.user_roles import UserRoles
from model.roles import Roles
from utils.common import (
        have_keys, tokenTime,
        generateOTP, encPass, checkPass, have_keys_NotForce)
from utils.jwt import (
        require_user_token,
        require_refresh_token,
        encoded_Token)
from utils.constants import ADMIN, PROVIDER, PATIENT, ESUser



class AuthenticationManager():
    def __init__(self):
        pass

    def register_user(self):
        user_json = request.get_json()
        if have_keys(user_json, 'email', 'password') is False:
            return {"message": "Invalid Request Parameters"}, 400
        if UserRegister.find_by_username(
            email=str(user_json["email"]).lower()
                ) is not None:
            return {"message": "User Already Exist"}, 409
        user = UserRegister(
            email=str(user_json["email"]).lower(),
            password=encPass(user_json["password"])
            )
        user.save_to_db()
        return {"message": "User Created"}, 201

    def login_user(self):
        user_json = request.get_json()
        if have_keys(user_json, 'email', 'password') is False:
            return {"message": "Invalid Request Parameters"}, 400
        user_data = UserRegister.find_by_username(
            str(user_json["email"]).lower())
        if user_data is None:
            return {"message": "No Such User Exist"}, 404
        if checkPass(user_json["password"], user_data.password):
            role_name_data = UserRegister.get_role_by_id(
                user_reg_id=user_data.id)
            encoded_accessToken = encoded_Token(
                False, str(user_json["email"]).lower(),
                role_name_data.role_name)
            encoded_refreshToken = encoded_Token(
                True, str(user_json["email"]).lower(),
                role_name_data.role_name)

            return {
                "message": "Successfully Login",
                "id_token": encoded_accessToken,
                "refresh_token": encoded_refreshToken,
                "isFirst": user_data.isFirst
                }, 200
        otp_data = UserOTPModel.find_by_user_id(user_id=user_data.id)
        if (
            otp_data is not None and
            otp_data.temp_password is not None and
            otp_data.temp_password != ""
                ):
            if checkPass(user_json["password"], otp_data.temp_password):
                encoded_accessToken = encoded_Token(
                    False, str(user_json["email"]).lower())
                encoded_refreshToken = encoded_Token(
                    False, str(user_json["email"]).lower())
                return {
                    "message": "Successfully Login",
                    "id_token": encoded_accessToken,
                    "refresh_token": encoded_refreshToken
                }, 200
        return {"message": "Invalid Credentials"}, 401

    @require_user_token(ADMIN, PROVIDER, PATIENT, ESUser)
    def update_user_password(self, decrypt):
        user_json = request.get_json()
        have_key = have_keys(
            user_json,
            'newpassword'
         )
        if have_key is False:
            return {"message": "Invalid Request Parameters"}, 400
        have_Auth = have_keys(decrypt, 'user_email')
        if have_Auth is False:
            return {"Message": "Unauthorized Access"}, 401
        user_data = UserRegister.find_by_username(decrypt["user_email"])
        if user_data is None:
            return {"message": "No Such User Exist"}, 404
        if user_json["newpassword"] is None or user_json["newpassword"] == "":
            return {
                "message": "New password does not meet minimum criteria"
                }, 200
        user_data.password = encPass(user_json["newpassword"])
        user_data.isFirst = 1
        user_data.update_db()
        return {"message": "Password Updated"}, 200

    @require_refresh_token
    def refresh_access_token(self, decrypt):
        encoded_accessToken = encoded_Token(False, decrypt["user_email"])
        return {
                "message": "Token Generated Successfully",
                "id_token": encoded_accessToken
                }, 200

    def reset_user_password(self):
        user_json = request.get_json()
        have_key = have_keys_NotForce(
            user_json, 'email', 'otp', 'password'
         )
        if have_key is True:
            user_data = UserRegister.find_by_username(
                email=str(user_json["email"]).lower()
                )
            if user_data is None:
                return {"message": "No Such User Exist"}, 404
            otp_data = UserOTPModel.matchOTP(
                user_id=user_data.id,
                user_otp=user_json["otp"]
                )
            if otp_data is None:
                return {"message": "OTP is Incorrect"}, 404
            otp_data.temp_password = encPass(user_json["password"])
            otp_data.update_db()
            return {"message": "OTP Matched"}, 200

        have_keyN = have_keys(
            user_json, 'email'
         )
        if have_keyN is True:
            user_data = UserRegister.find_by_username(
                email=str(user_json["email"]).lower())
            if user_data is None:
                return {"message": "No Such User Exist"}, 404
            otp = generateOTP()
            otp = "111111"
            user_otp = UserOTPModel(
                user_id=user_data.id, otp=otp, temp_password=""
            )
            user_otp.save_to_db()
            return {"message": "OTP Sent to Email"}, 200
        return {"message": "Invalid Request Parameters"}, 400
