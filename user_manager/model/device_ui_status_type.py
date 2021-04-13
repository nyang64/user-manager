from db import db
from sqlalchemy import String
from model.base_model import BaseModel


class DeviceUiStatusType(BaseModel):
    __tablename__ = "device_ui_status_types"
    __table_args__ = ({"schema": "ES"})
    name = db.Column('name', String(30), nullable=False)
    ui_id = db.Column('ui_id', db.String(50))

    @classmethod
    def all(cls) -> "DeviceUiStatusType":
        return cls.query.all()

    @classmethod
    def find_by_ui_id(cls, _ui_id) -> "DeviceUiStatusType":
        return cls.query.filter_by(ui_id=_ui_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
