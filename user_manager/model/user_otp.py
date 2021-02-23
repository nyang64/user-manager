from db import db
from sqlalchemy import Integer, String, desc
from model.base_model import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import InternalServerError


class UserOTPModel(BaseModel):
    __tablename__ = "user_otp"
    __table_args__ = ({"schema": "ES"})
    user_id = db.Column('user_id', Integer, nullable=False)
    otp = db.Column('otp', String(255), nullable=False)
    temp_password = db.Column('temp_password', String(255))

    @classmethod
    def matchOTP(cls, user_id: str, user_otp: str) -> "UserOTPModel":
        try:
            user_otp = cls.query.filter_by(
                user_id=user_id,
                otp=user_otp
                ).order_by(desc(cls.created_at)).limit(1).first()
        except SQLAlchemyError as error:
            db.session.rollback()
            raise InternalServerError(str(error))
        return user_otp

    @classmethod
    def find_by_user_id(cls, user_id: str) -> "UserOTPModel":
        try:
            user_otp = cls.query.filter_by(
                user_id=user_id
                ).order_by(desc(cls.created_at)).limit(1).first()
        except SQLAlchemyError as error:
            db.session.rollback()
            raise InternalServerError(str(error))
        return user_otp
