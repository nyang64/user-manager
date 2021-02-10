from model.user_registration import UserRegister
from utils.common import encPass
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import InternalServerError


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
