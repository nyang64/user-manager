from db import db
from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import backref
from datetime import datetime


class PatientsDevices(db.Model):
    __tablename__ = "patients_devices"
    __table_args__ = ({"schema": "ES"})
    id = db.Column(Integer, primary_key=True)
    patient_id = db.Column('patient_id', Integer, ForeignKey('ES.patients.id'), nullable=False)
    device_id = db.Column('device_id', Integer, ForeignKey('ES.devices.id'), nullable=False)   
    created_at = db.Column('created_at', DateTime, default = datetime.now(), nullable=False)
    patient = db.relationship(
        "Patient", backref=backref("patient_list", uselist=False)
    )
    device = db.relationship(
        "Devices", backref=backref("devices_list", uselist=False)
    )
    
    def save_patients_device(self) -> None:
        db.session.add(self)
        db.session.commit()
    