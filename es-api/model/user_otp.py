from db import db
from sqlalchemy import Integer, String, desc
from model.base_model import BaseModel


class UserOTPModel(BaseModel):
    __tablename__ = "user_otp"
    __table_args__ = ({"schema": "ES"})
    user_id = db.Column('user_id', Integer, nullable=False)
    otp = db.Column('otp', String(255), nullable=False)
    temp_password = db.Column('temp_password', String(255))

    @classmethod
    def matchOTP(cls, user_id: str, user_otp: str) -> "UserOTPModel":
        return cls.query.filter_by(
            user_id=user_id,
            otp=user_otp
            ).order_by(desc(cls.created_at)).limit(1).first()

    @classmethod
    def find_by_user_id(cls, user_id: str) -> "UserOTPModel":
        return cls.query.filter_by(
            user_id=user_id
            ).order_by(desc(cls.created_at)).limit(1).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def update_db(self) -> None:
        db.session.commit()
