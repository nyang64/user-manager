from sqlalchemy import Integer, ForeignKey, String
from db import db
from model.base_model import BaseModel


class AuthenticationToken(BaseModel):
    __tablename__ = "authentication_token"
    __table_args__ = ({"schema": "ES"})
    registration_id = db.Column('registration_id', Integer,
                                ForeignKey('ES.user_registration.id',
                                           ondelete='CASCADE'),
                                nullable=False)
    key = db.Column('key', String(120), nullable=False)
