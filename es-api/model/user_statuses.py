from sqlalchemy import Integer, ForeignKey
from db import db
from model.base_model import BaseModel


class UserStatUses(BaseModel):
    __tablename__ = "user_statuses"
    __table_args__ = ({"schema": "ES"})
    status_id = db.Column('status_id', Integer,
                          ForeignKey('ES.user_status_types.id',
                                     ondelete="CASCADE"),
                          nullable=False)
    user_id = db.Column('user_id', Integer,
                        ForeignKey('ES.users.id',
                                   ondelete="CASCADE"), nullable=False)
