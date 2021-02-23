from db import db
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import backref
from model.base_model import BaseModel


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
    def find_by_id(cls, id: str) -> "Providers":
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_providers(cls) -> "Providers":
        return cls.query.all()

    @classmethod
    def find_all(cls, id: str) -> "Providers":
        return cls.query.all()
