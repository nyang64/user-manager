from db import db
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import backref


class UserStatus(db.Model):
    __tablename__ = "status"
    id = db.Column(Integer, primary_key=True)
    status = db.Column(String(30), nullable=False)

    def __init__(self, status):
        self.status = status
