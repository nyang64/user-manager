from db import db
from sqlalchemy import Integer, String, ForeignKey, DateTime


class Devices(db.Model):
    __tablename__ = "devices"
    __table_args__ = ({"schema": "ES"})
    id = db.Column(Integer, primary_key=True)
    serial_number = db.Column('serial_number', String(12))
    encryption_key = db.Column('encryption_key', String(50))
    created_ts = db.Column('created_ts', DateTime)
    status = db.Column('status', Integer)