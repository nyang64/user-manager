from model.roles import Roles
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import InternalServerError, NotFound
from db import db


class RoleRepository():
    def save_Role(self, role_name):
        try:
            role_data = Roles(role_name=role_name)
            role_data.save_to_db()
            return role_data.id
        except SQLAlchemyError:
            db.session.rollback()
            # raise InternalServerError(str(error))
