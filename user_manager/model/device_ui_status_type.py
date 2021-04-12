from db import db
from sqlalchemy import String
from model.base_model import BaseModel


class DeviceUiStatusType(BaseModel):
    __tablename__ = "device_ui_status_types"
    __table_args__ = ({"schema": "ES"})
    name = db.Column('name', String(30), nullable=False)
    ui_id = db.Column('ui_id', db.String(50))

    @classmethod
    def find_by_name(cls, _name) -> "DeviceUiStatusType":
        return cls.query.filter_by(name=_name).first()

    @classmethod
    def all(cls) -> "DeviceUiStatusType":
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
