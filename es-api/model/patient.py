from db import db
from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import backref


class Patient(db.Model):
    __tablename__ = "patients"
    __table_args__ = ({"schema": "ES"})
    id = db.Column(Integer, primary_key=True)
    first_name = db.Column('first_name', String(30), nullable=False)
    last_name = db.Column('last_name', String(30), nullable=False)
    email = db.Column('email', String(100), nullable=False)
    mobile = db.Column('mobile', String(12), nullable=False)
    emergenct_contact_name = db.Column(
        'emergenct_contact_name', String(30), nullable=False)
    emergenct_contact_number = db.Column(
        'emergenct_contact_number', String(12), nullable=False)
    provider_id = db.Column('provider_id', Integer)
    external_auth_id = db.Column('external_auth_id', String(50))
    external_patient_id = db.Column('external_patient_id', String(50))
    date_of_birth = db.Column('date_of_birth', String(30))
    enrolled_date = db.Column('enrolled_date', DateTime)
    address_id = db.Column('address_id', Integer, ForeignKey('ES.address.id'))
    user_address = db.relationship(
        "Address", backref=backref("user_address")
    )
    user_id = db.Column('user_id', Integer, ForeignKey('ES.users.id'))
    user = db.relationship(
        "UserModel", backref=backref("user", uselist=False)
    )
