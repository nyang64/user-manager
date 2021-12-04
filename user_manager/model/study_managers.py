from db import db
from model.base_model import BaseModel
from sqlalchemy.orm import backref


class StudyManagers(BaseModel):
    __tablename__ = "study_managers"
    __table_args__ = {"schema": "ES"}
    user_id = db.Column(
        "user_id", db.Integer, db.ForeignKey("ES.users.id", ondelete="CASCADE")
    )
    address_id = db.Column(
        "address_id", db.Integer, db.ForeignKey("ES.addresses.id", ondelete="CASCADE")
    )
    facility_id = db.Column("facility_id", db.String(50),  nullable=True)
    user = db.relationship("Users", backref=backref("user_study_manager", uselist=False))
    address = db.relationship("Address", backref=backref("address_study_manager", uselist=False))

    @classmethod
    def all(cls) -> "StudyManagers":
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id: str) -> "StudyManagers":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> "StudyManagers":
        return cls.query.all()

    @classmethod
    def find_by_user_id(cls, _user_id) -> "StudyManagers":
        return cls.query.filter_by(user_id=_user_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
