from db import db
from sqlalchemy import String
from model.base_model import BaseModel


class Roles(BaseModel):
    __tablename__ = "roles"
    __table_args__ = ({"schema": "ES"})
    role_name = db.Column('role_name', String(30), nullable=False)
