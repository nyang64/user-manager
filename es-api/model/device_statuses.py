from sqlalchemy import Integer, ForeignKey
from db import db
from model.base_model import BaseModel


class DeviceStatUses(BaseModel):
    __tablename__ = "device_statuses"
    __table_args__ = ({"schema": "ES"})
    status_id = db.Column('status_id', Integer,
                          ForeignKey('ES.device_status_types.id',
                                     ondelete="CASCADE"),
                          nullable=False)
    device_id = db.Column('device_id', Integer,
                          ForeignKey('ES.devices.id',
                                     ondelete="CASCADE"),
                          nullable=False)
