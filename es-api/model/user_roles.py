from sqlalchemy import Integer, ForeignKey
from db import db
from model.base_model import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import InternalServerError, NotFound, Conflict


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

    @classmethod
    def find_by_user_id(cls, user_id: str) -> "UserRoles":
        try:
            user_role = cls.query.filter_by(user_id=user_id).first()
        except SQLAlchemyError as error:
            db.session.rollback()
            raise InternalServerError(str(error))
        return user_role

    def save_to_db(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            raise InternalServerError(str(error))