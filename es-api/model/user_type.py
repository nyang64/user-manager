from db import db
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import backref


class UserType(db.Model):
    __tablename__ = "user_type"
    __table_args__ = ({"schema": "ES"})
    id = db.Column(Integer, primary_key=True)
    type = db.Column(String(30), nullable=False)

    def __init__(type):
        self.type = type
