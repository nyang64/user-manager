from sqlalchemy import Integer, ForeignKey
from db import db
from model.base_model import BaseModel


class UserRoles(BaseModel):
    __tablename__ = "user_roles"
    __table_args__ = ({"schema": "ES"})
    role_id = db.Column('role_id', Integer,
                        ForeignKey('ES.roles.id',
                                   ondelete="CASCADE"),
                        nullable=False)
    user_id = db.Column('user_id', Integer,
                        ForeignKey('ES.users.id',
                                   ondelete="CASCADE"), nullable=False)
