from db import db
from sqlalchemy import String, UniqueConstraint
from model.base_model import BaseModel
import pdb


class Roles(BaseModel):
    __tablename__ = "role_types"
    __table_args__ = (UniqueConstraint('role_name'), {"schema": "ES"})
    role_name = db.Column('role_name', String(30), nullable=False)

    @classmethod
    def find_by_role_id(cls, role_id: str) -> "Roles":
        return cls.query.filter_by(id=role_id).first()

    @classmethod
    def find_by_name(cls, name: str) -> "Roles":
        return cls.query.filter_by(role_name=name).first()

    @classmethod
    def get_roleid(cls, role_name: str):
        return cls.query.filter_by(role_name=role_name).first()

    @classmethod
    def all(cls):
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
