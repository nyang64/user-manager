from db import db
from model.base_model import BaseModel
from sqlalchemy.orm import backref


class PatientsDevices(BaseModel):
    __tablename__ = "patients_devices"
    __table_args__ = {"schema": "ES"}
    patient_id = db.Column(
        "patient_id",
        db.Integer,
        db.ForeignKey("ES.patients.id", ondelete="CASCADE"),
        nullable=False,
    )
    device_serial_number = db.Column(
        "device_serial_number", db.String(50), nullable=False
    )
    is_active = db.Column(
        "is_active", db.Boolean, nullable=False, default=True
    )
    patient = db.relationship("Patient", backref=backref("patient_list"))
    device_metrics = db.defer(
        db.relationship("DeviceMetrics", backref="device_metrics")
    )
    device_statuses = db.defer(
        db.relationship("DeviceUiStatus", backref="device_ui_statuses")
    )

    @classmethod
    def device_in_use(cls, device_serial_no):
        device = (
            db.session.query(cls.id)
            .filter(cls.device_serial_number == device_serial_no)
            .first()
        )

        return True if device else False

    def all(cls) -> "PatientsDevices":
        return cls.query.all()

    @classmethod
    def find_by_patient_id(cls, _patient_id) -> "PatientsDevices":
        return cls.query.filter_by(id=_patient_id).first()

    @classmethod
    def find_all_devices_by_patient_id(cls, _patient_id) -> "PatientsDevices":
        return cls.query.filter_by(patient_id=_patient_id).all()

    @classmethod
    def find_record_by_patient_id(cls, _patient_id) -> "PatientsDevices":
        return cls.query.filter_by(patient_id=_patient_id, is_active=True).first()

    @classmethod
    def find_by_device_serial_number(cls, _device_sn) -> "PatientDevices":
        return db.session.query(cls).filter_by(device_serial_number=_device_sn).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
