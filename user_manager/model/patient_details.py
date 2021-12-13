from db import db
from model.base_model import BaseModel


class PatientDetails(BaseModel):
    __tablename__ = "patient_details"
    __table_args__ = {"schema": "ES"}

    patient_id = db.Column(
        "patient_id",
        db.Integer,
        db.ForeignKey("ES.patients.id", ondelete="CASCADE"),
    )

    mobile_model = db.Column("mobile_model", db.String(20), nullable=False)
    mobile_os_version = db.Column("mobile_os_version", db.String(20), nullable=False)
    other_phone = db.Column("other_phone", db.String(12), nullable=False)
    pa_setting_back = db.Column("pa_setting_back", db.String(12), nullable=True)
    pa_setting_front = db.Column("pa_setting_front", db.String(12), nullable=True)
    shoulder_strap_back = db.Column("shoulder_strap_back", db.String(12), nullable=True)
    shoulder_strap_front = db.Column("shoulder_strap_front", db.String(12), nullable=True)
    starter_kit_lot_number = db.Column("starter_kit_lot_number", db.String(20), nullable=True)
    upper_patch_setting = db.Column("upper_patch_setting", db.String(20), nullable=False)
    enrollment_notes = db.Column("enrollment_notes", db.String(300), nullable=False)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def all(cls) -> "PatientDetails":
        return cls.query.all()

    @classmethod
    def find_by_patient_id(cls, _patient_id) -> "PatientDetails":
        return cls.query.filter_by(patient_id=_patient_id).first()

    def update(self, **kwargs):
        for field, value in kwargs.items():
            setattr(self, field, value)
