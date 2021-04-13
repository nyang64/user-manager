from db import db
from sqlalchemy import String
from model.base_model import BaseModel


class DeviceMetricType(BaseModel):
    __tablename__ = "device_metrics_types"
    __table_args__ = ({"schema": "ES"})
    name = db.Column('name', String(30), nullable=False)

    @classmethod
    def all(cls) -> "DeviceMeticType":
        return cls.query.all()

    @classmethod
    def find_by_name(cls, _name) -> "DeviceMeticType":
        return cls.query

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
