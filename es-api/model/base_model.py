from db import db
from datetime import datetime

class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column('id', db.Integer, primary_key=True)
    created_at = db.Column('created_at', db.DateTime, default=datetime.now)