from db import db
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import backref
from model.base_model import BaseModel


class Providers(BaseModel):
    __tablename__ = "providers"
    __table_args__ = ({"schema": "ES"})
    id = db.Column(Integer, primary_key=True)
    user_id = db.Column('user_id', Integer, ForeignKey('ES.users.id'))
    facility_id = db.Column('facility_id', Integer)  # relationship peding
    user = db.relationship(
        "User", backref=backref("user_provider", uselist=False)
    )
# first_name, lASt_name, facility_id, phONe, email, scope_id, user_id

    def __init__(self, user_id, facility_id, created_at):
        self.user_id = user_id
        self.facility_id = facility_id
        self.created_at = created_at

    @classmethod
    def find_by_id(cls, id: str) -> "Providers":
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls, id: str) -> "Providers":
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def update_db(self) -> None:
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()
