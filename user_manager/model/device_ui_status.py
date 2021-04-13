from db import db
from model.base_model import BaseModel


class DeviceUiStatus(BaseModel):
    __tablename__ = "device_ui_statuses"
    __table_args__ = ({"schema": "ES"})
    device_serial_number = db.Column(
        'device_serial_number',
        db.String(50),
        nullable=False
    )
    ui_status_id = db.Column('ui_status_id', db.String(50), nullable=False)
    recorded_at = db.Column('recorded_at', db.DateTime)
    receiver_id = db.Column('receiver_id', db.String(50))
    receiver_recorded_at = db.Column('receiver_recorded_at', db.DateTime)

    @classmethod
    def all(cls) -> "DeviceUiStatus":
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
