from db import db
from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import backref
from model.base_model import BaseModel


class Patient(BaseModel):
    __tablename__ = "patients"
    __table_args__ = ({"schema": "ES"})
    user_id = db.Column('user_id', Integer,
                        ForeignKey('ES.users.id', ondelete="CASCADE"))
    provider_id = db.Column('provider_id', Integer,
                            ForeignKey('ES.providers.id', ondelete="CASCADE"))
    emergency_contact_name = db.Column('emergency_contact_name',
                                       String(30),
                                       nullable=False)
    emergency_contact_number = db.Column('emergency_contact_phone',
                                         String(12),
                                         nullable=False)
    date_of_birth = db.Column('date_of_birth',
                              String(30))
    enrolled_date = db.Column('enrolled_at',
                              DateTime)
    users = db.relationship("Users",
                            backref=backref("users_patient", uselist=False))

    def save_patient(self) -> None:
        db.session.add(self)
        db.session.commit()
