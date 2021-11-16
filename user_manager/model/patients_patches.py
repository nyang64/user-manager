from db import db
from sqlalchemy.orm import backref
from model.base_model import BaseModel


class PatientsPatches(BaseModel):
    __tablename__ = "patients_patches"
    __table_args__ = {"schema": "ES"}
    patch_lot_number = db.Column(
        "patch_lot_number", db.String(20), nullable=False
    )
    is_applied = db.Column(
        "is_applied", db.Boolean, default=False
    )
    patient_id = db.Column(
        "patient_id",
        db.Integer,
        db.ForeignKey("ES.patients.id", ondelete="CASCADE"),
    )
    # Date and time when the patient returned the used patches back to ES
    patch_returned_date = db.Column("patch_returned_date", db.DateTime)

    # Date and time when the ES manufacturing shipped new patches to the patient
    patch_shipped_date = db.Column("patch_shipped_date", db.DateTime)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def all(cls) -> "PatientsPatches":
        return cls.query.all()

    @classmethod
    def find_by_patient_id(cls, _patient_id):
        return cls.query.filter_by(patient_id=_patient_id).all()
