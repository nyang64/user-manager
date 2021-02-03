from db import db
from sqlalchemy import String
from model.base_model import BaseModel


class Devices(BaseModel):
    __tablename__ = "devices"
    __table_args__ = ({"schema": "ES"})
    serial_number = db.Column('serial_number', String(12))
    encryption_key = db.Column('encryption_key', String(50))
