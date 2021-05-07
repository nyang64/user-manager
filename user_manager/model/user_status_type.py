from db import db
from model.base_model import BaseModel


class UserStatusType(BaseModel):
    __tablename__ = "user_status_types"
    __table_args__ = {"schema": "ES"}
    name = db.Column("name", db.String(30), nullable=False)

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def find_by_name(cls, _name):
        return db.session.query(cls).filter_by(name=_name).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
