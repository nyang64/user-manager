from db import db
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import backref
from model.base_model import BaseModel
from model.user_registration import UserRegister
from model.users import Users


class Providers(BaseModel):
    __tablename__ = "providers"
    __table_args__ = ({"schema": "ES"})
    user_id = db.Column('user_id', Integer,
                        ForeignKey('ES.users.id', ondelete="CASCADE"))
    facility_id = db.Column('facility_id', Integer,
                            ForeignKey('ES.facilities.id', ondelete="CASCADE"))
    user = db.relationship(
        "Users", backref=backref("user_provider", uselist=False)
    )

    @classmethod
    def all(cls) -> "Providers":
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id: str) -> "Providers":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_providers(cls) -> "Providers":
        return cls.query.all()

    @classmethod
    def find_all(cls, id: str) -> "Providers":
        return cls.query.all()

    @classmethod
    def find_by_user_id(cls, _user_id) -> "Providers":
        return cls.query.filter_by(user_id=_user_id).first()

    @classmethod
    def find_by_email(cls, email: str) -> "Providers":
        user_registration = UserRegister.find_by_email(email)
        user = Users.find_by_registration_id(user_registration.id)
        return cls.find_by_user_id(user.id)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
