from db import db
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import backref
from model.base_model import BaseModel


class PatientsDevices(BaseModel):
    __tablename__ = "patients_devices"
    __table_args__ = ({"schema": "ES"})
    patient_id = db.Column('patient_id', Integer,
                           ForeignKey('ES.patients.id', ondelete="CASCADE"),
                           nullable=False)
    device_id = db.Column('device_id', Integer,
                          ForeignKey('ES.devices.id', ondelete="CASCADE"),
                          nullable=False)
    patient = db.relationship(
        "Patient", backref=backref("patient_list", uselist=False)
    )
    device = db.relationship(
        "Devices", backref=backref("devices_list", uselist=False)
    )

    def save_patients_device(self) -> None:
        db.session.add(self)
        db.session.commit()
