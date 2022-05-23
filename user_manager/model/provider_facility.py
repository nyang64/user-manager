from db import db
from model.base_model import BaseModel
from model.providers import Providers
from model.users import Users
from sqlalchemy.orm import backref
from sqlalchemy import and_

class ProviderFacility(BaseModel):
    __tablename__ = "provider_facility"
    __table_args__ = {"schema": "ES"}
    provider_id = db.Column(
        "provider_id", db.Integer, db.ForeignKey("ES.providers.id", ondelete="CASCADE")
    )
    facility_id = db.Column(
        "facility_id", db.Integer, db.ForeignKey("ES.facilities.id", ondelete="CASCADE")
    )
    provider = db.relationship("Providers", backref=backref("provider_provider", uselist=False))
    facility = db.relationship("Facilities", backref=backref("provider_facility", uselist=False))
    is_primary = db.Column("is_primary", db.Boolean, nullable=False, default=False)

    @classmethod
    def find_by_provID_facID(cls, providerId, facilityId) -> "ProviderFacility":
        result = cls.query.filter(ProviderFacility.provider_id == providerId) \
                          .filter(ProviderFacility.facility_id == facilityId).first()
        return result
    @classmethod
    def find_facility_ids_by_provider_id(cls, provider_id) -> "ProviderFacility":
        result = cls.query.with_entities(ProviderFacility.facility_id, ProviderFacility.is_primary).filter_by(provider_id=provider_id).all()
        result = [(id, isPrimary) for id, isPrimary in result]
        return result


    @classmethod
    def find_by_facility_id(cls, _facility_id) -> "ProviderFacility":
        return cls.query.filter_by(facility_id=_facility_id).all()


    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
