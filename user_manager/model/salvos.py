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
    device_serial_number = db.Column('device_serial_number',
                                     String)
    clinician_verified_at = db.Column("clinician_verified_at",
                                      db.DateTime)
    raw_data_location = db.Column('raw_data_location',
                                  String(100))
    pdf_location = db.Column('pdf_location',
                             String(100))
    receiver_recorded_at = db.Column('receiver_recorded_at',
                                     db.DateTime)
    receiver_sent_at = db.Column('receiver_sent_at',
                                 db.DateTime)
    receiver_id = db.Column('receiver_id',
                            String(20))
    shock_count = db.Column('shock_count',
                            Integer)
