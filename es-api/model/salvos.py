from sqlalchemy import Integer, String, ForeignKey
from db import db
from model.base_model import BaseModel


class Salvos(BaseModel):
    __tablename__ = "salvos"
    __table_args__ = ({"schema": "ES"})
    therapy_report_id = db.Column('therapy_report_id', Integer,
                                  ForeignKey('ES.therapy_reports.id',
                                             ondelete="CASCADE"),
                                  nullable=False)
    device_id = db.Column('device_id', Integer,
                          ForeignKey('ES.devices.id',
                                     ondelete="CASCADE"),
                          nullable=False)
    raw_data_location = db.Column('raw_data_location', String(100))
    pdf_location = db.Column('pdf_location', String(100))
