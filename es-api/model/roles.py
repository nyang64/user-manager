from db import db
from sqlalchemy import String, UniqueConstraint
from model.base_model import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import InternalServerError, NotFound


class Roles(BaseModel):
    __tablename__ = "roles"
    __table_args__ = (UniqueConstraint('role_name'), {"schema": "ES"})
    role_name = db.Column('role_name', String(30), nullable=False)

    def save_to_db(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()

    @classmethod
    def find_by_role_id(cls, role_id: str) -> "Roles":
        try:
            roles = cls.query.filter_by(id=role_id).first()
        except SQLAlchemyError as error:
            db.session.rollback()
            raise InternalServerError(str(error))
        return roles
