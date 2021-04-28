from db import db
from model.base_model import BaseModel
from sqlalchemy import ForeignKey, Integer


class TherapyReport(BaseModel):
    __tablename__ = "therapy_reports"
    __table_args__ = {"schema": "ES"}
    device_serial_number = db.Column("device_serial_number", Integer, nullable=False)
    patient_id = db.Column(
        "patient_id",
        Integer,
        ForeignKey("ES.patients.id", ondelete="CASCADE"),
        nullable=False,
    )
