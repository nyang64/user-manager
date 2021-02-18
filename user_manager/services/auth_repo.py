from model.user_registration import UserRegister
from utils.common import encPass
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import InternalServerError, NotFound, Unauthorized
from utils.common import checkPass, auth_response_model
from utils.jwt import encoded_Token
from model.user_otp import UserOTPModel


class AuthRepository():
    def __init__(self):
        pass

    def register_user(self, email, password):
        try:
            user_data = UserRegister(email=email,
                                     password=encPass(password))
            UserRegister.flush_db(user_data)
            return user_data.id
        except SQLAlchemyError as error:
            raise InternalServerError(str(error))

    def User_login(self, data: UserRegister) -> auth_response_model:
        user_data = UserRegister.find_by_username(
            str(data.email).lower())
        if user_data is None:
            raise NotFound("No Such User Exist")
        role_name_data = UserRegister.get_role_by_id(
            user_reg_id=user_data.id)
        if role_name_data is None:
            raise Unauthorized("No Such User Allowed")
        if checkPass(data.password, user_data.password):
            encoded_accessToken = encoded_Token(
                False, str(data.email).lower(),
                role_name_data.role_name)
            encoded_refreshToken = encoded_Token(
                True, str(data.email).lower(),
                role_name_data.role_name)
            response_model = auth_response_model(
                message="Successfully Login",
                id_token=encoded_accessToken,
                refresh_token=encoded_refreshToken,
                isFirstTimeLogin=user_data.isFirst
            )
            return response_model.toJsonObj()
        otp_data = UserOTPModel.find_by_user_id(user_id=user_data.id)
        if (
            otp_data is not None and
            otp_data.temp_password is not None and
            otp_data.temp_password != ""
                ):
            if checkPass(data.password, otp_data.temp_password):
                encoded_accessToken = encoded_Token(
                    False, str(data.email).lower(),
                    role_name_data.role_name)
                encoded_refreshToken = encoded_Token(
                    True, str(data.email).lower(),
                    role_name_data.role_name)
                response_model = auth_response_model(
                    message="Successfully Login",
                    id_token=encoded_accessToken,
                    refresh_token=encoded_refreshToken,
                    isFirstTimeLogin=user_data.isFirst
                    )
                return response_model.toJsonObj()
            else:
                raise Unauthorized("Invalid Credentials")
        raise Unauthorized("Invalid Credentials")

    def refresh_user_token(self, data):
        encoded_accessToken = encoded_Token(False, data)
        response_model = auth_response_model(
            message="Token Refreshed Successfully",
            id_token=encoded_accessToken)
        return response_model.toJsonObj()

    def update_password(self, user_email, newpassword):
        user_data = UserRegister.find_by_username(user_email)
        if user_data is None:
            raise NotFound("No Such User Exist")
        user_data.password = encPass(newpassword)
        user_data.isFirst = False
        user_data.update_db()
        UserOTPModel.deleteAll_OTP(user_id=user_data.id)
        return {"message": "Password Updated"}, 200
