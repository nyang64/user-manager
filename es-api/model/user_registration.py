from db import db
from sqlalchemy import String, Integer, Boolean
from model.base_model import BaseModel
from model.roles import Roles
from model.user_roles import UserRoles
from model.users import Users
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import InternalServerError

class UserRegister(BaseModel):
    __tablename__ = "user_registration"
    __table_args__ = ({"schema": "ES"})
    email = db.Column('email', String(50), nullable=False, unique=True)
    password = db.Column('password', String(255), nullable=False)
    isFirst = db.Column('isFirst', Boolean, default=True)

    @classmethod
    def find_by_username(cls, email: str) -> "UserRegister":
        try:
            user_registration_data = cls.query.filter_by(email=email).first()
        except SQLAlchemyError as error:
            db.session.rollback()
            raise InternalServerError(str(error))
        return user_registration_data

    def save_to_db(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            raise InternalServerError(str(error))

    def update_db(self) -> None:
        try:
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            raise InternalServerError(str(error))
        
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
