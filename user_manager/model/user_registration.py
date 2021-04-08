from sqlalchemy import String, Boolean
from model.base_model import BaseModel
from db import db
import logging


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
