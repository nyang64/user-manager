from db import db
from sqlalchemy import String
from model.base_model import BaseModel


class ProviderRoleTypes(BaseModel):
    __tablename__ = "provider_role_types"
    __table_args__ = ({"schema": "ES"})
    name = db.Column('name', String(30), nullable=False)

    @classmethod
    def find_by_name(cls, _name) -> "ProviderRoleTypes":
        return cls.query.filter_by(id=_name).first()

    @classmethod
    def all(cls) -> "ProviderRoleTypes":
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
