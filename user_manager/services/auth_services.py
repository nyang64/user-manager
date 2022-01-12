import logging
from datetime import datetime, timedelta

import pytz
from model.user_otp import UserOTPModel
from model.user_registration import UserRegister
from model.users import Users
from model.user_status import UserStatus
from model.user_status_type import UserStatusType
from services.repository.db_repositories import DbRepository
from sqlalchemy.exc import SQLAlchemyError
from utils.common import auth_response_model, checkPass, encPass
from utils.jwt import encoded_Token
from utils import constants
from utils.cache import cache
from utils.send_mail import send_password_reset_email
from werkzeug.exceptions import Conflict, InternalServerError, NotFound, Unauthorized

utc = pytz.UTC

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class AuthServices(DbRepository):
    def __init__(self):
        pass

    def register_new_user(self, email, password):
        """ Flush the user"""
        exist_email = UserRegister.find_by_email(email)
        if bool(exist_email) is True:
            msg = str(email) + " already exist"
            raise Conflict(msg)
        try:
            user_data = UserRegister(email=email, password=encPass(password))
            self.flush_db(user_data)
            return user_data.id
        except SQLAlchemyError as error:
            logging.error(error)
            raise InternalServerError(str(error))

    def delete_registration(self, reg_id, session):
        exist_data = UserRegister.find_by_id(reg_id)
        if bool(exist_data) is False:
            raise NotFound("user record not found")
        exist_data.deactivated = True
        if session:
            session.add(exist_data)
            return session
        else:
            self.save_db(exist_data)

    def add_otp(self, user_otp):
        self.save_db(user_otp)

    def User_login(self, data: UserRegister) -> auth_response_model:
        user_data = UserRegister.find_by_email(str(data.email).lower())

        if user_data is None:
            raise NotFound("No Such User Exist")

        # Check to see if user is deactivated
        # If disabled return error message
        if user_data.deactivated:
            response = auth_response_model(
                message="Account Deactivated",
                locked=False,
                deactivated=True,
                id_token="",
                user_status="",
                isFirstTimeLogin="",
            )
            return response.toJsonObj(), 403

        # Check session and to see if we need to proceed further with authentication.
        # If the account is already locked or multiple login failures, return with a
        # error message
        if user_data.locked or self.reached_max_incorrect_login_attempts(user_data):
            response = auth_response_model(
                message="Account Locked",
                locked=True,
                deactivated=False,
                id_token="",
                user_status="",
                isFirstTimeLogin="",
            )
            return response.toJsonObj(), 401

        logger.debug(user_data.__dict__)
        user_detail = Users.find_by_registration_id(user_data.id)

        user_roles = user_detail.roles
        if user_roles is None:
            raise Unauthorized("No Such User Allowed")

        role_name = user_roles[0].role.role_name
        logger.debug(role_name)

        if checkPass(data.password, user_data.password):
            encoded_accessToken = encoded_Token(
                False, str(data.email).lower(), role_name
            )
            encoded_refreshToken = encoded_Token(
                True, str(data.email).lower(), role_name
            )
            #clean up session
            self.reset_session(user_data.email)
            response_model = auth_response_model(
                message="Successfully Logged In",
                first_name=user_detail.first_name,
                last_name=user_detail.last_name,
                id_token=encoded_accessToken,
                refresh_token=encoded_refreshToken,
                isFirstTimeLogin=user_data.isFirst,
                locked=user_data.locked,
                deactivated=user_data.deactivated,
                user_role=role_name,
            )
            return response_model.toJsonObj()

        otp_data = UserOTPModel.find_by_user_id(user_id=user_data.id)
        if (
            otp_data is not None
            and otp_data.temp_password
            and otp_data.temp_password != ""
        ):
            if checkPass(data.password, otp_data.temp_password):
                encoded_accessToken = encoded_Token(
                    False, str(data.email).lower(), role_name
                )
                encoded_refreshToken = encoded_Token(
                    True, str(data.email).lower(), role_name
                )
                self.reset_session(user_data.email)
                response_model = auth_response_model(
                    message="Successfully Logged In",
                    id_token=encoded_accessToken,
                    first_name=user_detail.first_name,
                    last_name=user_detail.last_name,
                    refresh_token=encoded_refreshToken,
                    isFirstTimeLogin=user_data.isFirst,
                    user_role=role_name,
                )
                return response_model.toJsonObj()
            else:
                raise Unauthorized("Invalid Credentials")
        raise Unauthorized("Invalid Credentials")

    def reached_max_incorrect_login_attempts(self, user_data):
        try:
            # Users account is not locked.
            # Check if the session as user data already
            user_session = self.get_user_session(user_data.email)
            logging.info(f"User session: {user_session}")
            session_end = user_session["session_end_at"]
            current_time = datetime.utcnow().timestamp()

            logging.error(f"Session end time: {session_end}")
            logging.error(f"Current time: {current_time}")

            if current_time <= session_end:
                print("Incrementing login count")
                user_session = self.increment_failed_login_count(user_session)
                cache.set(user_data.email, user_session)

                if user_session["attempted_login_count"] >= constants.MAX_FAILED_LOGINS_ALLOWED:
                    logging.error("Locking the account because of number failed attempts")
                    self.lock_account(user_data)
                    return True
            elif current_time >= session_end:
                print("Resetting the session as current time is greater than the session end time")
                self.reset_session(user_data.email)
        except Exception as e:
            logging.error(f"Error updating user session for {user_data.email}: {e}")

    def get_user_session(self, email):
        user_ses_dict = cache.get(email)
        current_time = datetime.utcnow()
        lifetime = timedelta(minutes=constants.SESSION_EXPIRATION_TIME_IN_MINUTES)

        if user_ses_dict is None:
            user_ses_dict = {
                "session_start_at": current_time.timestamp(),
                "session_end_at": (current_time + lifetime).timestamp()
            }
            cache.set(email, user_ses_dict)
        else:
            if user_ses_dict["session_start_at"] >= user_ses_dict["session_end_at"]:
                print("Resetting the session as session start time is greater than the end time")
                self.reset_session(email)

        return user_ses_dict

    def increment_failed_login_count(self, user_session):
        login_count = user_session.get("attempted_login_count") or 0
        user_session["attempted_login_count"] = login_count + 1
        print(user_session)
        return user_session

    def lock_account(self, user_data):
        if user_data:
            user_ses = cache.get(user_data.email)
            user_ses["session_locked"] = True
            user_data.locked = True
            user_data.save_to_db()
            return user_ses

    def reset_session(self, email):
        cache.delete(email)

    def refresh_user_token(self, data):
        encoded_access_token = encoded_Token(False, data)
        msg = "Token Refreshed Successfully"
        response_model = auth_response_model(message=msg, id_token=encoded_access_token)
        return response_model.toJsonObj()

    def update_password(self, user_email, newpassword, send_email):
        user_data = UserRegister.find_by_email(user_email)
        if user_data is None:
            raise NotFound("No Such User Exist")
        user_data.password = encPass(newpassword)
        user_data.isFirst = False
        self.update_db(user_data)
        UserOTPModel.deleteAll_OTP(user_id=user_data.id)

        if send_email:
            user = Users.find_by_registration_id(user_data.id)
            send_password_reset_email(user.first_name, user.last_name, user_email, user_email, newpassword)
        return {"message": "Password Updated"}, 200

    def update_otp_data(self, otp_data):
        self.update_db(otp_data)
        return "OTP Matched"

    def unlock_account(self, user_email):
        # Update the database
        user = Users.find_by_email(user_email)
        if user:
            user.registration.locked = False
            user.save_to_db()

        # Check the session and make sure the lock from the session is removed too.
        self.reset_session(user_email)

    def patient_portal_login(self, data: UserRegister) -> auth_response_model:
        user_data = UserRegister.find_by_email(str(data.email).lower())
        if user_data is None:
            raise NotFound("No Such User Exist")

        # Check to see if user is deactivated
        # If disabled return error message
        if user_data.deactivated:
            response = auth_response_model(
                message="Account Deactivated",
                locked=False,
                deactivated=True,
                id_token="",
                user_status="",
                isFirstTimeLogin=""
            )
            return response.toJsonObj(), 403

        # Check session and to see if we need to proceed further with authentication.
        logger.debug(user_data.__dict__)
        user_detail = Users.find_by_registration_id(user_data.id)

        user_roles = user_detail.roles
        if user_roles is None:
            raise Unauthorized("No Such User Allowed")

        role_name = user_roles[0].role.role_name
        logger.debug(role_name)

        if role_name not in [constants.PATIENT, constants.PROVIDER]:
            response = auth_response_model(
                message="User with role " + role_name + " is not allowed to access this content",
                locked=False,
                deactivated=False,
                id_token="",
                user_status="",
                isFirstTimeLogin=""
            )
            return response.toJsonObj(), 403

        # Get the password from secret manager
        if data.password == constants.PATIENT_PORTAL_LOGIN_PASSWORD:
            access_token = encoded_Token(
                False, str(data.email).lower(), role_name
            )
            refresh_token = encoded_Token(
                True, str(data.email).lower(), role_name
            )
            self.reset_session(user_data.email)
            response_model = auth_response_model(
                message="Successfully Logged In",
                id_token=access_token,
                first_name=user_detail.first_name,
                last_name=user_detail.last_name,
                refresh_token=refresh_token,
                isFirstTimeLogin=user_data.isFirst,
                user_role=role_name
            )
            return response_model.toJsonObj()
        raise Unauthorized("Invalid Credentials")



