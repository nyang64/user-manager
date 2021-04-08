from db import db
from sqlalchemy import Integer, String, desc
from model.base_model import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import InternalServerError
from datetime import datetime, timedelta
import os
from config import read_environ_value
import logging


class UserOTPModel(BaseModel):
    __tablename__ = "user_otps"
    __table_args__ = ({"schema": "ES"})
    user_id = db.Column('user_id', Integer, nullable=False)
    otp = db.Column('otp', String(255), nullable=False)
    temp_password = db.Column('temp_password', String(255))

    @classmethod
    def matchOTP(cls, user_id: str) -> "UserOTPModel":
        try:
            user_otp = cls.query.filter_by(
                user_id=user_id
                ).order_by(desc(cls.created_at)).limit(1).first()
        except SQLAlchemyError as error:
            logging.error(error)
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
            logging.error(error)
            db.session.rollback()
            raise InternalServerError(str(error))
        return user_otp

    @classmethod
    def find_list_by_user_id(cls, user_id: str) -> "UserOTPModel":
        try:
            value = os.environ.get('SECRET_MANAGER_ARN')
            now = datetime.now()
            d = now - timedelta(
                hours=int(read_environ_value(
                    value, "OTP_LIMIT_HOURS")),
                minutes=int(read_environ_value(
                    value, "OTP_LIMIT_MINUTES")))
            user_otp_list = cls.query.filter(
                    user_id == user_id,
                    d <= BaseModel.created_at).count()
        except SQLAlchemyError as error:
            logging.error(error)
            db.session.rollback()
            raise InternalServerError(str(error))
        return user_otp_list

    @classmethod
    def deleteAll_OTP(cls, user_id):
        try:
            cls.query.filter(user_id == user_id).\
                delete(synchronize_session=False)
            db.session.commit()
        except SQLAlchemyError as error:
            logging.error(error)
            raise InternalServerError(str(error))
