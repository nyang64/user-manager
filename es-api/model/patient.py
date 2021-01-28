from db import db
from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import backref
from datetime import datetime


class Patient(db.Model):
    __tablename__ = "patients"
    __table_args__ = ({"schema": "ES"})
    id = db.Column(Integer, primary_key=True)
    user_id = db.Column('user_id', Integer, ForeignKey('ES.users.id'))
    provider_id = db.Column('provider_id', Integer, ForeignKey('ES.user.id'))    
    emergenct_contact_name = db.Column(
        'emergenct_contact_name', String(30), nullable=False)
    emergenct_contact_number = db.Column(
        'emergenct_contact_phone', String(12), nullable=False)
    date_of_birth = db.Column('date_of_birth', String(30))
    enrolled_date = db.Column('enrolled_at', DateTime)
    created_at = db.Column('created_at', DateTime, default = datetime.now(), nullable=False)
    user = db.relationship(
        "UserModel", backref=backref("user", uselist=False)
    )
    
