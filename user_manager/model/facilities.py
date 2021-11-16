from db import db
from model.base_model import BaseModel


class Facilities(BaseModel):
    __tablename__ = "facilities"
    __table_args__ = {"schema": "ES"}
    address_id = db.Column(
        "address_id",
        db.Integer,
        db.ForeignKey("ES.addresses.id", ondelete="CASCADE"),
        nullable=True,
    )
    external_facility_id = db.Column(
        "external_facility_id",
        db.String(10),
        nullable=False,
    )
    on_call_phone = db.Column("on_call_phone", db.String(12), nullable=False)
    name = db.Column("name", db.String(100))
    is_active = db.Column(
        "is_active", db.Boolean, nullable=True, default=True
    )

    @classmethod
    def find_by_id(cls, _id) -> "Facilities":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_external_id(cls, _ext_id) -> "Facilities":
        return cls.query.filter_by(external_facility_id=_ext_id).first()

    @classmethod
    def all(cls) -> "Facilities":
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
