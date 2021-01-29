from db import db
from sqlalchemy import Integer, String, DateTime


class UserRegister(db.Model):
    __tablename__ = "user_registration"
    __table_args__ = ({"schema": "ES"})
    id = db.Column(Integer, primary_key=True)
    username = db.Column('username', String(50), nullable=False, unique=True)
    password = db.Column('password', String(255), nullable=False)
    created_at = db.Column('created_at', DateTime)

    def __init__(self, username, password, created_at):
        self.username = username
        self.password = password
        self.created_at = created_at

    @classmethod
    def find_by_username(cls, username: str) -> "UserRegister":
        return cls.query.filter_by(username=username).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def update_db(self) -> None:
        db.session.commit()
