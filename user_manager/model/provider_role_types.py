from db import db
from sqlalchemy import String
from model.base_model import BaseModel


class ProviderRoleTypes(BaseModel):
    __tablename__ = "provider_role_types"
    __table_args__ = ({"schema": "ES"})
    name = db.Column('name', String(30), nullable=False)
