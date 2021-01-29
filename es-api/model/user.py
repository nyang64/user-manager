from db import db
from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import backref
import uuid
from datetime import datetime

def generate_uuid():
    return str(uuid.uuid4())

class User(db.Model):
    __tablename__ = "users"
    __table_args__ = ({"schema": "ES"})
    id = db.Column(Integer, primary_key=True)
    registration_id = db.Column('registration_id', Integer, ForeignKey('ES.user_registration.id'))
    first_name = db.Column('first_name', String(30), nullable=False)
    last_name = db.Column('last_name', String(30), nullable=False)
    phone_number = db.Column('phone_number', String(12), nullable=False)
    email = db.Column('email', String(100), nullable=False)
    created_at = db.Column('created_at', DateTime, default = datetime.now(), nullable=False)
    uuid = db.Column('uuid', String(50), default = generate_uuid(), unique = True, nullable = False)
    
    def __init__(self, first_name, last_name, phone_number, email):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        
    def save_user(self) -> None:
        db.session.add(self)
        db.session.commit()
