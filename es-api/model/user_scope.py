from db import db
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import backref


class UserScope(db.Model):
    __tablename__ = "scope"
    id = db.Column(Integer, primary_key=True)
    scope = db.Column(String(30), nullable=False)

    def __init__(self, scope):
        self.scope = scope
