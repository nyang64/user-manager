from sqlalchemy import Integer, ForeignKey, String
from db import db
from model.base_model import BaseModel


class Facilities(BaseModel):
    __tablename__ = "facilities"
    __table_args__ = ({"schema": "ES"})
    address_id = db.Column('address_id', Integer,
                           ForeignKey('ES.address.id', ondelete="CASCADE"),
                           nullable=False)
    name = db.Column('name', String(100))
