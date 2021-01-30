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
from utils.common import have_keys, tokenTime, generateOTP, encPass, checkPass
from utils.jwt import require_user_token, require_refresh_token
import datetime
import jwt
import bcrypt

user_schema = UserSchema()


class AuthenticationManager():
    def __init__(self):
        pass

    def register_user(self):
        user_json = request.get_json()
        if have_keys(user_json, 'username', 'password') is False:
            return {"message": "Invalid Request Parameters"}, 200
        if UserRegister.find_by_username(
            username=user_json["username"]
                ) is not None:
            return {"message": "User Already Exist"}, 400
        # password = bytes(user_json["password"], 'utf-8')
        # salt = bcrypt.gensalt()
        # hashed = bcrypt.hashpw(password, salt)
        user = UserRegister(
            user_json["username"],
            encPass(user_json["password"]),
            datetime.datetime.now()
            )
        user.save_to_db()
        return {"message": "User Created"}, 201

    def login_user(self):
        user_json = request.get_json()
        if have_keys(user_json, 'username', 'password') is False:
            return {"message": "Invalid Request Parameters"}, 400
        udt = UserRegister.find_by_username(user_json["username"])
        if udt is None:
            return {"message": "No Such User Exist"}, 404
        # db_pass = bytes(udt.password, 'utf-8')
        # inp_pass = bytes(user_json["password"], 'utf-8')
        # if bcrypt.checkpw(
        #         inp_pass,
        #         db_pass.decode().encode('utf-8')
        #         ):
        if checkPass(user_json["password"], udt.password):
            encoded_accessToken = jwt.encode({
                "username": user_json["username"],
                "exp": (tokenTime(False))
                }, "C718D5FDDEC279567385BE3E52894")
            encoded_refreshToken = jwt.encode({
                "username": user_json["username"],
                "exp": (tokenTime(True))
                 }, "9EA72AD96C39A87A1AFF153983592")

            return {
                "message": "Successfully Login",
                "id_token": encoded_accessToken,
                "refresh_token": encoded_refreshToken
                }, 200
        otpDT = UserOTPModel.find_by_user_id(user_id=udt.id)
        if (
            otpDT is not None and
            otpDT.temp_password is not None and
            otpDT.temp_password != ""
                ):
            # db_pass = bytes(otpDT.temp_password, 'utf-8')
            # if bcrypt.checkpw(
            #         inp_pass,
            #         db_pass.decode().encode('utf-8')
            #         ):
            if checkPass(user_json["password"], otpDT.temp_password):
                encoded_accessToken = jwt.encode({
                    "username": user_json["username"],
                    "exp": (tokenTime(False))
                }, "C718D5FDDEC279567385BE3E52894")
                encoded_refreshToken = jwt.encode({
                    "username": user_json["username"],
                    "exp": (tokenTime(True))
                }, "9EA72AD96C39A87A1AFF153983592")
                return {
                    "message": "Successfully Login",
                    "id_token": encoded_accessToken,
                    "refresh_token": encoded_refreshToken
                }, 200
        return {"message": "Invalid Credentials"}, 401

    @require_user_token
    def update_user_password(self, decryp):
        user_json = request.get_json()
        have_key = have_keys(
            user_json,
            'newpassword'
         )
        if have_key is False:
            return {"message": "Invalid Request Parameters"}, 400
        print("dec", decryp)
        have_Auth = have_keys(decryp, 'username')
        if have_Auth is False:
            return {"Message": "Unauthorized Access"}, 401
        dt = UserRegister.find_by_username(decryp["username"])
        if dt is None:
            return {"message": "No Such User Exist"}, 404
        # db_pass = bytes(dt.password, 'utf-8')
        # inp_pass = bytes(user_json["oldpassword"], 'utf-8')
        # if bcrypt.checkpw(
        #         inp_pass,
        #         db_pass.decode().encode('utf-8')
        #         ) is False:
        
        # if checkPass(user_json["oldpassword"], dt.password):
            # return {"message": "Incorrect Password"}, 200
        if user_json["newpassword"] is None or user_json["newpassword"] == "":
            return {
                "message": "New password does not meet minimum criteria"
                }, 200
        dt.password = encPass(user_json["newpassword"])
        dt.update_db()
        return {"message": "Password Updated"}, 200

    @require_refresh_token
    def refresh_access_token(self):
        user_json = request.get_json()
        have_key = have_keys(
            user_json, 'username'
         )
        if have_key is False:
            return {"message": "Invalid Request Parameters"}, 400
        encoded_accessToken = jwt.encode({
            "username": user_json["username"],
            "exp": (tokenTime(False))
            }, "C718D5FDDEC279567385BE3E52894")
        return {
                "message": "Token Generated Successfully",
                "id_token": encoded_accessToken
                }, 200

    def reset_user_password(self):
        user_json = request.get_json()
        have_key = have_keys(
            user_json, 'username', 'otp', 'password'
         )
        if have_key is True:
            dt = UserRegister.find_by_username(username=user_json["username"])
            if dt is None:
                return {"message": "No Such User Exist"}, 404
            dta = UserOTPModel.matchOTP(
                user_id=dt.id,
                user_otp=user_json["otp"]
                )
            if dta is None:
                return {"message": "OTP is in Correct"}, 404
            # password = bytes(user_json["password"], 'utf-8')
            # salt = bcrypt.gensalt()
            # hashed = bcrypt.hashpw(password, salt)
            dta.temp_password = encPass(user_json["password"])
            dta.update_db()
            return {"message": "OTP Matched"}, 200

        have_keyN = have_keys(
            user_json, 'username'
         )
        if have_keyN is True:
            dt = UserRegister.find_by_username(username=user_json["username"])
            if dt is None:
                return {"message": "No Such User Exist"}, 404
            otp = generateOTP()
            otp = "111111"
            userOTP = UserOTPModel(
                dt.id, otp, datetime.datetime.now(), ""
            )
            userOTP.save_to_db()
            return {"message": "OTP Sent to Email"}, 200
        return {"message": "Invalid Request Parameters"}, 400

# 200 -> Successful
# 404 -> User doesn't exist
# 401 -> Unauthorized
