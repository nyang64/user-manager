from werkzeug.exceptions import InternalServerError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import String, Boolean
from model.base_model import BaseModel
from model.user_roles import UserRoles
from model.roles import Roles
from model.users import Users
from db import db


class UserRegister(BaseModel):
    __tablename__ = "registrations"
    __table_args__ = ({"schema": "ES"})
    email = db.Column('email', String(50), nullable=False, unique=True)
    password = db.Column('password', String(255), nullable=False)
    isFirst = db.Column('isFirst', Boolean, default=True)

    @classmethod
    def find_by_email(cls, email: str) -> "UserRegister":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, reg_id):
        return cls.query.filter_by(id=reg_id).first()

    @classmethod
    def get_role_by_id(cls, user_reg_id: str) -> "UserRoles":
        try:
            users_data = Users().find_by_registration_id(
                    registration_id=user_reg_id)
            if users_data is None:
                return False
            user_role_data = UserRoles().find_by_user_id(
                user_id=users_data.id)
            if user_role_data is None:
                return False
            role_name_data = Roles().find_by_role_id(
                role_id=user_role_data.role_id)
            if role_name_data is None:
                return False
            return role_name_data
        except Exception as error:
            raise InternalServerError(str(error))
