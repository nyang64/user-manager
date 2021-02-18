from sqlalchemy import String
from db import db
from model.base_model import BaseModel


class DeviceStatusType(BaseModel):
    __tablename__ = "device_status_types"
    __table_args__ = ({"schema": "ES"})
    name = db.Column('name', String(30))
