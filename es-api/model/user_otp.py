from db import db
from sqlalchemy import Integer, String, DateTime


class UserOTPModel(db.Model):
    __tablename__ = "user_otp"
    __table_args__ = ({"schema": "ES"})
    id = db.Column(Integer, primary_key=True)
    user_id = db.Column('user_id', Integer, nullable=False)
    otp = db.Column('otp', String(255), nullable=False)
    created_at = db.Column('created_at', DateTime)

    def __init__(self, user_id, otp, created_at):
        self.user_id = user_id
        self.otp = otp
        self.created_at = created_at

    @classmethod
    def matchOTP(cls, user_id: str, user_otp: str) -> "UserOTPModel":
        return cls.query.filter_by(
            user_id=user_id,
            otp=user_otp
            ).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def update_db(self) -> None:
        db.session.commit()
