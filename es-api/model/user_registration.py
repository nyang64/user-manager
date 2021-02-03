from db import db
from sqlalchemy import String, Integer
from model.base_model import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import InternalServerError, NotFound, Conflict


class UserRegister(BaseModel):
    __tablename__ = "user_registration"
    __table_args__ = ({"schema": "ES"})
    email = db.Column('email', String(50), nullable=False, unique=True)
    password = db.Column('password', String(255), nullable=False)
    isFirst = db.Column('isFirst', Integer, default=0)

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
