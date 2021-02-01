from db import db
from sqlalchemy import String, Integer
from model.base_model import BaseModel


class UserRegister(BaseModel):
    __tablename__ = "user_registration"
    __table_args__ = ({"schema": "ES"})
    email = db.Column('email', String(50), nullable=False, unique=True)
    password = db.Column('password', String(255), nullable=False)
    isFirst = db.Column('isFirst', Integer, default=0)

    @classmethod
    def find_by_username(cls, email: str) -> "UserRegister":
        return cls.query.filter_by(email=email).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def update_db(self) -> None:
        db.session.commit()
