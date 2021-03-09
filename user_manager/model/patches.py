from db import db
from sqlalchemy import Integer, ForeignKey
from model.base_model import BaseModel


class Patches(BaseModel):
    __tablename__ = "patches"
    __table_args__ = ({"schema": "ES"})
    patient_device_id = db.Column('patient_device_id',
                                  Integer,
                                  ForeignKey('ES.patients_devices.id',
                                             ondelete="CASCADE"))
