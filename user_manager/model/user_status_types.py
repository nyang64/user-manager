from db import db
from model.base_model import BaseModel


class UserStatusType(BaseModel):
    __tablename__ = "user_status_types"
    __table_args__ = {"schema": "ES"}
    name = db.Column("name", db.String(30), nullable=False)
