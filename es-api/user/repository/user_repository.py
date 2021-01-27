from model.user import User
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import InternalServerError
from db import db

class UserRepository():
    def create_user(self, first_name, last_name, phone_number, email):
        try:
            user_data = User(first_name, last_name, phone_number, email)
            print('create_user')
            User.save_user(user_data)
            print('user created')
        except SQLAlchemyError as error:
            db.session.rollback()
            raise InternalServerError(error)