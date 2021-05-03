from db import db
from model.base_model import BaseModel


class DeviceMetric(BaseModel):
    __tablename__ = "device_metrics"
    __table_args__ = {"schema": "ES"}
    device_serial_number = db.Column(
        "device_serial_number", db.String(50), nullable=False
    )
    metric_id = db.Column(
        "device_metrics_id",
        db.Integer,
        db.ForeignKey("ES.device_metrics_types.id", ondelete="CASCADE"),
    )
    metric_value = db.Column("device_metrics_data", db.String(50))
    recorded_at = db.Column("recorded_at", db.DateTime)
    receiver_id = db.Column("receiver_id", db.String(50))
    receiver_recorded_at = db.Column("receiver_recorded_at", db.DateTime)

    @classmethod
    def all(cls) -> "DeviceMetric":
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
