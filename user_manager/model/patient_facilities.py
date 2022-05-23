from db import db
from model.base_model import BaseModel
from sqlalchemy.orm import backref
from sqlalchemy import and_

class PatientFacilities(BaseModel):
    __tablename__ = "patient_facilities"
    __table_args__ = {"schema": "ES"}
    patient_id = db.Column(
        "patient_id", db.Integer, db.ForeignKey("ES.patients.id", ondelete="CASCADE")
    )
    facility_id = db.Column(
        "facility_id", db.Integer, db.ForeignKey("ES.facilities.id", ondelete="CASCADE")
    )
    is_active = db.Column(
        "is_active", db.Boolean, nullable=False, default=True
    )
    patient = db.relationship("Patient", backref=backref("patient_patient", uselist=False))
    facility = db.relationship("Facilities", backref=backref("patient_facilities", uselist=False))

    @classmethod
    def all(cls) -> "PatientFacilities":
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id) -> "PatientFacilities":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_facility_id_by_patient_id(cls, _patient_id) -> "PatientFacilities":
        return cls.query.filter_by(patient_id=_patient_id)\
                        .filter_by(is_active=True)\
                        .all()

    @classmethod
    def find_by_facility_id(cls, _facility_id) -> "PatientFacilities":
        return cls.query.filter_by(facility_id=_facility_id).all()


    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
