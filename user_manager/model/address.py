from db import db
from sqlalchemy import String, ForeignKey, Integer
from model.base_model import BaseModel
from sqlalchemy.orm import column_property


class Address(BaseModel):
    __tablename__ = "addresses"
    __table_args__ = ({"schema": "ES"})
    user_id = db.Column('user_id', Integer,
                        ForeignKey('ES.users.id', ondelete="CASCADE"))
    street_address_1 = db.Column('street_address_1', String(100))
    street_address_2 = db.Column('street_address_2', String(100))
    # full_address = column_property(street_address_1 + " " + street_address_2)
    city = db.Column('city', String(100))
    state = db.Column('state', String(50))
    country = db.Column('country', String(20))
    postal_code = db.Column('postal_code', String(10))

    @classmethod
    def find_by_id(cls, _id: str) -> "Address":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_user_id(cls, _user_id) -> "Address":
        return cls.query.filter_by(id=_user_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
