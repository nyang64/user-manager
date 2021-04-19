from db import db
from sqlalchemy import Integer, ForeignKey
from sqlalchemy import String
from model.base_model import BaseModel


class Patches(BaseModel):
    __tablename__ = "patches"
    __table_args__ = ({"schema": "ES"})
    patch_serial_number = db.Column('patch_serial_number', String(30), nullable=False)
    patient_device_id = db.Column('patient_device_id',
                                  Integer,
                                  ForeignKey('ES.patients_devices.id',
                                             ondelete="CASCADE"))
