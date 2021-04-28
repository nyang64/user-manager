from db import db
from model.base_model import BaseModel


class UserRegister(BaseModel):
    __tablename__ = "registrations"
    __table_args__ = {"schema": "ES"}
    email = db.Column("email", db.String(50), nullable=False, unique=True)
    password = db.Column("password", db.String(255), nullable=False)
    isFirst = db.Column("isFirst", db.Boolean, default=True)

    @classmethod
    def find_by_email(cls, email: str) -> "UserRegister":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, reg_id):
        return cls.query.filter_by(id=reg_id).first()
