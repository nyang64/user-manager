from db import db
from sqlalchemy import String
from model.base_model import BaseModel


class UserScope(BaseModel):
    __tablename__ = "scope"
    __table_args__ = ({"schema": "ES"})
    scope = db.Column(String(30), nullable=False)
