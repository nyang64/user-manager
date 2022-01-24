import logging
import os
from datetime import datetime

from config import read_environ_value
from flask import request

# Do not remove used at time of migration
from model.facilities import Facilities
from model.user_otp import UserOTPModel
from model.user_registration import UserRegister
from model.users import Users
from schema.login_schema import user_login_schema
from schema.update_password_schema import user_update_schema
from services.auth_services import AuthServices
from utils.common import encPass, generateOTP, have_keys, have_keys_NotForce
from utils.constants import ADMIN, ESUSER, PATIENT, PROVIDER, STUDY_MANAGER, CUSTOMER_SERVICE
from utils.jwt import encoded_Token, require_refresh_token, require_user_token
from utils.send_mail import send_otp
from utils.validation import validate_request
from werkzeug.exceptions import InternalServerError
from datetime import timedelta


class AuthOperation:
    def __init__(self):
        self.auth_obj = AuthServices()

    def login_user(self):
        login_object = user_login_schema.validate_data(request.json)

        return self.auth_obj.User_login(login_object)

    @require_refresh_token
    def refresh_token(self, decrypt):
        encoded_accessToken = encoded_Token(False, decrypt["user_email"])
        return (
            {
                "message": "Token Generated Successfully",
                "id_token": encoded_accessToken,
            },
            200,
        )

    @require_refresh_token
    def user_refresh_token(self, decrypt):
        request_data = validate_request()
        role = request_data["role"]
        encoded_accessToken = encoded_Token(False, decrypt["user_email"], user_role=role)
        return (
            {
                "message": "Token Generated Successfully",
                "id_token": encoded_accessToken,
            },
            200,
        )


    @require_user_token(ADMIN, CUSTOMER_SERVICE, STUDY_MANAGER)
    def update_and_email_set_password(self, decrypt):
        logging.info("Updating User Password")
        user_json = request.json
        try:
            user_email = user_json["user_login"]
            newpassword = user_json["password"]
        except Exception as ex:
            logging.error(ex)
            raise InternalServerError("Invalid Request Parameters")

        user_update_schema.validate_data(
            {"user_email": user_email, "newpassword": newpassword}
        )
        self.auth_obj.update_password(user_email, newpassword, send_email=True)
        logging.info("Updated password")
        return {"message": "Password Updated"}, 200

    @require_user_token(ADMIN, PROVIDER, PATIENT, ESUSER, CUSTOMER_SERVICE, STUDY_MANAGER)
    def update_user_password(self, decrypt):
        logging.info("Updating User Password")
        user_json = request.json
        try:
            newpassword = user_json["newpassword"]
        except Exception as ex:
            logging.error(ex)
            raise InternalServerError("Invalid Request Parameters")
        if "user_email" not in decrypt:
            return {"Message": "Unauthorized Access"}, 401
        user_update_schema.validate_data(
            {"user_email": decrypt["user_email"], "newpassword": newpassword}
        )
        self.auth_obj.update_password(decrypt["user_email"], newpassword, send_email=False)
        logging.info("Updated password")
        return {"message": "Password Updated"}, 200

    @require_user_token(ADMIN, PROVIDER, PATIENT, ESUSER)
    def delete(self, decrypt):
        self.auth_obj.reset_session(decrypt["user_email"])
        return {"message": "Logged out"}, 200

    @require_user_token(ADMIN, PROVIDER, PATIENT, ESUSER, STUDY_MANAGER, CUSTOMER_SERVICE)
    def validate_token(self, decrypt):
        return {"message": "Token is valid"}, 200

    @require_user_token(ADMIN)
    def unlock_account(self, decrypt):
        req_json = request.json
        try:
            self.auth_obj.unlock_account(req_json["user_email"])
            return {"message": "Unlocked user account"}, 200
        except Exception as e:
            logging.error(f"Error unlocking the account: {e}")
            return {"message": "Er"}, 400

    def reset_user_password(self):
        value = os.environ.get("SECRET_MANAGER_ARN")
        user_json = request.json
        have_key = have_keys_NotForce(user_json, "email", "otp", "password")
        if have_key is True:
            user_data = UserRegister.find_by_email(
                email=str(user_json["email"]).lower()
            )
            if user_data is None:
                return {"message": "No Such User Exist"}, 404
            otp_data = UserOTPModel.matchOTP(user_id=user_data.id)
            if otp_data is None:
                logging.warning("OTP is incorrect")
                return {"message": "OTP is Incorrect"}, 404
            elif otp_data.otp != user_json.get("otp"):
                logging.warning("OTP is incorrect")
                return {"message": "OTP is Incorrect"}, 404
            now = datetime.now()
            expiration_time = now - timedelta(
                hours=int(read_environ_value(value, "OTP_EXPIRATION_TIME_HOURS")),
                minutes=int(read_environ_value(value, "OTP_EXPIRATION_TIME_MINUTES")),
            )
            logging.info("Created {}".format(otp_data.created_at))
            logging.info("Expiration {}".format(expiration_time))
            epoch_ct = otp_data.created_at.timestamp()
            epoch_et = expiration_time.timestamp()
            logging.info("Created in EPCOH {}".format(otp_data.created_at))
            logging.info("Expiration EPOCH {}".format(expiration_time))
            if epoch_ct < epoch_et:
                return {"message": "OTP is Expired"}, 410
            otp_data.temp_password = encPass(user_json.get("password"))
            msg = self.auth_obj.update_otp_data(otp_data)
            return {"message": msg}, 200

        have_keyN = have_keys(user_json, "email")
        if have_keyN is True:
            user_data = UserRegister.find_by_email(
                email=str(user_json["email"]).lower()
            )
            if user_data is None:
                logging.warning("No such user exist")
                return {"message": "No Such User Exist"}, 404
            otp_cnt = UserOTPModel.find_list_by_user_id(user_data.id)
            if int(otp_cnt) >= int(read_environ_value(value, "OTP_LIMIT")):
                logging.warning("OTP Limit exceeded")
                return {"message": "OTP Limit Reached"}, 429
            user_detail = Users.get_user_by_registration_id(user_reg_id=user_data.id)
            otp = generateOTP()
            send_otp(
                user_detail.first_name,
                user_data.email,
                "Your One Time Password of Element Science App",
                otp,
            )
            logging.info("OTP sent to email")
            user_otp = UserOTPModel(user_id=user_data.id, otp=otp, temp_password="")
            self.auth_obj.add_otp(user_otp)
            return {"message": "OTP Sent to Email"}, 200
        return {"message": "Invalid Request Parameters"}, 400

    def patient_portal_login(self):
        login_object = user_login_schema.validate_data(request.json)
        return self.auth_obj.patient_portal_login(login_object)

    @require_user_token(ADMIN, CUSTOMER_SERVICE, STUDY_MANAGER)
    def send_password_to_cs(self, token):
        user_json = validate_request()
        try:
            user_email = user_json["user_email"]
        except Exception as ex:
            logging.error(ex)
            return {"message": "Invalid Request Parameters"}, 400

        self.auth_obj.send_user_password_to_cs(user_email)
        return {"message": "Success"}, 200


