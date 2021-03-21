from db import db
from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import backref
from model.base_model import BaseModel


class Patient(BaseModel):
    __tablename__ = "patients"
    __table_args__ = ({"schema": "ES"})
    user_id = db.Column('user_id', Integer,
                        ForeignKey('ES.users.id', ondelete="CASCADE"), nullable=False)
    provider_id = db.Column('provider_id', Integer,
                            ForeignKey('ES.providers.id', ondelete="CASCADE"), nullable=False)
    emergency_contact_name = db.Column('emergency_contact_name',
                                       String(30),
                                       nullable=False)
    emergency_contact_number = db.Column('emergency_contact_phone',
                                         String(12),
                                         nullable=False)
    gender = db.Column('gender',
                       String(12))
    date_of_birth = db.Column('date_of_birth',
                              String(30), nullable=False)
    enrolled_date = db.Column('enrolled_at',
                              DateTime,
                              default=db.func.now())
    gender = db.Column('gender', String(30), nullable=False)
    users = db.relationship("Users",
                            backref=backref("users_patient", uselist=False))

    @classmethod
    def find_by_id(cls, patient_id):
        return db.session.query(cls).filter_by(
            id=patient_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
