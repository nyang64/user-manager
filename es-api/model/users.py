from db import db
from sqlalchemy import Integer, String, ForeignKey
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

    def save_user(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email: str) -> "Users":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_registration_id(cls, registration_id: str) -> "Users":
        return cls.query.filter_by(registration_id=registration_id).first()

    @classmethod
    def find_by_user_id(cls, user_id: str) -> "Users":
        return cls.query.filter_by(id=user_id).first()
