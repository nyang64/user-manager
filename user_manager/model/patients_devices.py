from db import db
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import backref
from model.base_model import BaseModel


class PatientsDevices(BaseModel):
    __tablename__ = "patients_devices"
    __table_args__ = ({"schema": "ES"})
    patient_id = db.Column('patient_id', db.Integer,
                           ForeignKey('ES.patients.id', ondelete="CASCADE"),
                           nullable=False)
    device_serial_number = db.Column('device_serial_number',
                                     db.String(50),
                                     nullable=False)
    patient = db.relationship(
        "Patient", backref=backref("patient_list")
    )

    @classmethod
    def check_device_assigned(cls, device_serial_no):
        return db.session.query(cls.id).filter(
            cls.device_serial_number == device_serial_no).first()
