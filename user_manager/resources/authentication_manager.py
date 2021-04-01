from schema.login_schema import user_login_schema
from schema.update_password_schema import user_update_schema
from utils.jwt import require_user_token, require_refresh_token, encoded_Token
from utils.constants import ADMIN, PROVIDER, PATIENT, ESUSER
from werkzeug.exceptions import InternalServerError
from flask import request
from utils.common import have_keys, have_keys_NotForce, encPass, generateOTP
from utils.send_mail import send_otp
from model.user_registration import UserRegister
from model.users import Users
from model.user_otp import UserOTPModel
from services.auth_services import AuthServices
from datetime import datetime, timedelta
import os
from config import read_environ_value
import logging
# Do not remove used at time of migration
from model.facilities import Facilities


class AuthOperation():
    def __init__(self):
        self.auth_obj = AuthServices()

    def login_user(self):
        login_object = user_login_schema.validate_data(request.get_json())
        return self.auth_obj.User_login(login_object)

    @require_refresh_token
    def refresh_token(self, decrypt):
        encoded_accessToken = encoded_Token(False, decrypt["user_email"])
        return {
                "message": "Token Generated Successfully",
                "id_token": encoded_accessToken
                }, 200

    @require_user_token(ADMIN, PROVIDER, PATIENT, ESUSER)
    def update_user_password(self, decrypt):
        logging.info('Updating User Password')
        user_json = request.get_json()
        try:
            newpassword = user_json["newpassword"]
        except Exception as ex:
            self.logging.error(ex)
            raise InternalServerError("Invalid Request Parameters")
        if 'user_email' not in decrypt:
            return {"Message": "Unauthorized Access"}, 401
        user_update_schema.validate_data({
                "user_email": decrypt["user_email"],
                "newpassword": newpassword
            })
        self.auth_obj.update_password(decrypt["user_email"], newpassword)
        logging.info('Updated password')
        return {"message": "Password Updated"}, 200

    def reset_user_password(self):
        value = os.environ.get('SECRET_MANAGER_ARN')
        user_json = request.get_json()
        have_key = have_keys_NotForce(
            user_json, 'email', 'otp', 'password'
         )
        if have_key is True:
            user_data = UserRegister.find_by_email(
                email=str(user_json["email"]).lower()
                )
            if user_data is None:
                return {"message": "No Such User Exist"}, 404
            otp_data = UserOTPModel.matchOTP(
                user_id=user_data.id
                )
            if otp_data is None:
                logging.warning('OTP is incorrect')
                return {"message": "OTP is Incorrect"}, 404
            elif otp_data.otp != user_json.get("otp"):
                logging.warning('OTP is incorrect')
                return {"message": "OTP is Incorrect"}, 404
            now = datetime.now()
            expiration_time = now - timedelta(
                hours=int(read_environ_value(
                    value, "OTP_EXPIRATION_TIME_HOURS")),
                minutes=int(read_environ_value(
                    value, "OTP_EXPIRATION_TIME_MINUTES")))
            logging.info('Created {}'.format(otp_data.created_at))
            logging.info('Expiration {}'.format(expiration_time))
            epoch_ct = otp_data.created_at.timestamp()
            epoch_et = expiration_time.timestamp()
            logging.info('Created in EPCOH {}'.format(otp_data.created_at))
            logging.info('Expiration EPOCH {}'.format(expiration_time))
            if epoch_ct < epoch_et:
                return {"message": "OTP is Expired"}, 410
            otp_data.temp_password = encPass(user_json.get("password"))
            msg = self.auth_obj.update_otp_data(otp_data)
            return {"message": msg}, 200

        have_keyN = have_keys(
            user_json, 'email'
         )
        if have_keyN is True:
            user_data = UserRegister.find_by_email(
                email=str(user_json["email"]).lower())
            if user_data is None:
                logging.warning('No such user exist')
                return {"message": "No Such User Exist"}, 404
            otp_cnt = UserOTPModel.find_list_by_user_id(user_data.id)
            if int(otp_cnt) >= int(read_environ_value(value, "OTP_LIMIT")):
                logging.warning('OTP Limit exceeded')
                return {"message": "OTP Limit Reached"}, 429
            user_detail = Users.getUserById(user_reg_id=user_data.id)
            otp = generateOTP()
            send_otp(
                user_detail.first_name,
                user_data.email,
                "Your One Time Password of Element Science App",
                otp)
            logging.info('OTP sent to email')
            user_otp = UserOTPModel(
                user_id=user_data.id, otp=otp, temp_password=""
            )
            self.auth_obj.add_otp(user_otp)
            return {"message": "OTP Sent to Email"}, 200
        return {"message": "Invalid Request Parameters"}, 400
