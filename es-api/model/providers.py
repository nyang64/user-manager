from db import db
from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import backref
from datetime import datetime
from model.base_model import BaseModel


class Providers(BaseModel):
    __tablename__ = "providers"
    __table_args__ = ({"schema": "ES"})
    user_id = db.Column('user_id', Integer, ForeignKey('ES.users.id'))
    facility_id = db.Column('facility_id', Integer) # relationship peding
    user = db.relationship(
        "User", backref=backref("user_provider", uselist=False)
    )