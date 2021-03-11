from db import db


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column('id', db.Integer, primary_key=True)
    created_at = db.Column('created_at',
                           db.DateTime(timezone=True),
                           default=db.func.now(),
                           nullable=False,
                           server_default=db.text('now()'))
    updated_on = db.Column('updated_at', db.DateTime(timezone=True),
                           default=db.func.now(),
                           onupdate=db.func.now(),
                           server_default=db.text('now()'))
