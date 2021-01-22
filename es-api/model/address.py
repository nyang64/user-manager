from db import db
from sqlalchemy import Integer, String, ForeignKey


class Address(db.Model):
    __tablename__ = "address"
    __table_args__ = ({"schema": "ES"})
    id = db.Column(Integer, primary_key=True)
    street_address_1 = db.Column('street_address_1', String(100))
    street_address_2 = db.Column('street_address_2', String(100))
    city = db.Column('city', String(100))
    state = db.Column('state', String(50))
    country = db.Column('country', String(20))
    postal_code = db.Column('postal_code', String(10))