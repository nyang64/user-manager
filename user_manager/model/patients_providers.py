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

    @classmethod
    def find_by_patient_id(cls, _patient_id) -> "PatientsProviders":
        return cls.query.filter_by(patient_id=_patient_id).first()

    @classmethod
    def find_by_patient_and_role_id(cls, _patient_id, _role_id) -> "PatientsProviders":
        return cls.query.filter_by(patient_id=_patient_id, provider_role_id=_role_id).first()
