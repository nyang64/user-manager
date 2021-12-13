import logging

from db import db
from model.base_model import BaseModel


class Newsletters(BaseModel):
    __tablename__ = "newsletters"
    __table_args__ = {"schema": "ES"}
    user_id = db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("ES.users.id", ondelete="CASCADE"),
        nullable=False,
    )
    day_at = db.Column("day_at", db.Integer, nullable=False, default=0)

    @classmethod
    def all(cls) -> "Newsletters":
        return cls.query.all()

    @classmethod
    def all_records(cls) -> "Newsletters":
        return db.session.query(cls).all()

    @classmethod
    def find_by_id(cls, _id: str) -> "Newsletters":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_user_id(cls, _user_id) -> "Newsletters":
        return cls.query.filter_by(user_id=_user_id).first()

    @classmethod
    def unenroll_by_user_id(self, _user_id):
        pass

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
