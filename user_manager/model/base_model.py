from db import db
from sqlalchemy import exc
from werkzeug.exceptions import InternalServerError


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column('id', db.Integer, primary_key=True)
    created_at = db.Column('created_at',
                           db.DateTime,
                           default=db.func.now(),
                           nullable=False)
    updated_on = db.Column('updated_at', db.DateTime,
                           default=db.func.now(),
                           onupdate=db.func.now())
