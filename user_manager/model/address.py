from db import db
from model.base_model import BaseModel


class Address(BaseModel):
    __tablename__ = "addresses"
    __table_args__ = {"schema": "ES"}
    user_id = db.Column(
        "user_id", db.Integer, db.ForeignKey("ES.users.id", ondelete="CASCADE")
    )
    street_address_1 = db.Column("street_address_1", db.String(100))
    street_address_2 = db.Column("street_address_2", db.String(100))
    city = db.Column("city", db.String(100))
    state = db.Column("state", db.String(50))
    country = db.Column("country", db.String(20))
    postal_code = db.Column("postal_code", db.String(10))

    @classmethod
    def find_by_id(cls, _id: str) -> "Address":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_user_id(cls, _user_id) -> "Address":
        return cls.query.filter_by(id=_user_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
