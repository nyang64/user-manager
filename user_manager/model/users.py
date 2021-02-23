from db import db
from sqlalchemy import Integer, String, ForeignKey
from werkzeug.exceptions import NotFound, InternalServerError
import uuid
from model.base_model import BaseModel


class Users(BaseModel):
    __tablename__ = "users"
    __table_args__ = ({"schema": "ES"})
    registration_id = db.Column('registration_id', Integer,
                                ForeignKey('ES.user_registration.id',
                                           ondelete="CASCADE"))
    first_name = db.Column('first_name', String(30),
                           nullable=False)
    last_name = db.Column('last_name', String(30),
                          nullable=False)
    phone_number = db.Column('phone_number', String(12),
                             nullable=False)
    uuid = db.Column('uuid', String(50), default=str(uuid.uuid4()),
                     unique=True, nullable=False)

    @classmethod
    def find_by_email(cls, email: str) -> "Users":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_registration_id(cls, registration_id: str) -> "Users":
        return cls.query.filter_by(registration_id=registration_id).first()

    @classmethod
    def find_by_user_id(cls, user_id: str) -> "Users":
        return cls.query.filter_by(id=user_id).first()

    @classmethod
    def check_user_exist(cls, user_id):
        return db.session.query(cls).filter_by(
            id=user_id).first()
        
    @classmethod
    def getUserById(cls, user_reg_id):
        try:
            user = cls.find_by_registration_id(
                registration_id=user_reg_id)
            if user is None:
                raise NotFound("User Details Not Found")
            return user
        except Exception:
            raise InternalServerError("Something Went Wrong")
