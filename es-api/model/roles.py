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
