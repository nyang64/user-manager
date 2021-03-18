from db import db
from sqlalchemy import Integer, ForeignKey
from model.base_model import BaseModel


class PatientsProviders(BaseModel):
    __tablename__ = "patients_providers"
    __table_args__ = ({"schema": "ES"})
    patient_id = db.Column('patient_id',
                           Integer,
                           ForeignKey('ES.patients.id',
                                      ondelete="CASCADE"))
    provider_role_id = db.Column('provider_role_id',
                                 Integer,
                                 ForeignKey('ES.provider_role_types.id',
                                            ondelete="CASCADE"))
    provider_id = db.Column('provider_id',
                            Integer,
                            ForeignKey('ES.providers.id',
                                       ondelete="CASCADE"))

    @classmethod
    def all(cls) -> "PatientsProviders":
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id) -> "PatientsProviders":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
