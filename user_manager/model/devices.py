from db import db
from sqlalchemy import String, Integer
from model.base_model import BaseModel


class Devices(BaseModel):
    __tablename__ = "devices"
    __table_args__ = ({"schema": "ES"})
    serial_number = db.Column('serial_numbers', Integer,
                              unique=True, nullable=False)
    encryption_key = db.Column('encryption_key', String(100),
                               nullable=False)
