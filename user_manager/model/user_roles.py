from sqlalchemy import Integer, ForeignKey
from db import db
from model.base_model import BaseModel


class UserRoles(BaseModel):
    __tablename__ = "user_roles"
    __table_args__ = ({"schema": "ES"})
    role_id = db.Column('role_id', Integer,
                        ForeignKey('ES.role_types.id',
                                   ondelete="CASCADE"),
                        nullable=False)
    user_id = db.Column('user_id', Integer,
                        ForeignKey('ES.users.id',
                                   ondelete="CASCADE"), nullable=False)
    role = db.relationship("Roles", backref="roles", uselist=False)

    @classmethod
    def find_by_user_id(cls, user_id: str) -> "UserRoles":
        user_role = cls.query.filter_by(user_id=user_id).first()
        return user_role

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
