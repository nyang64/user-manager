from db import db
from sqlalchemy import String, UniqueConstraint
from model.base_model import BaseModel


class Roles(BaseModel):
    __tablename__ = "role_types"
    __table_args__ = (UniqueConstraint('role_name'), {"schema": "ES"})
    role_name = db.Column('role_name', String(30), nullable=False)

    @classmethod
    def find_by_role_id(cls, role_id: str) -> "Roles":
        roles = cls.query.filter_by(id=role_id).first()
        return roles

    @classmethod
    def get_roleid(cls, role_name: str):
        return db.session.query(cls.id).filter_by(
            role_name=role_name).scalar()
