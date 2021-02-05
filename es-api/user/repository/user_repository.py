from model.users import Users
from sqlalchemy.exc import SQLAlchemyError
from model.user_roles import UserRoles
from werkzeug.exceptions import InternalServerError, NotFound
from db import db
from utils.common import generate_uuid
from common.common_repo import CommonRepo


class UserRepository():
    def __init__(self):
        self.commonObj = CommonRepo()

    def save_user(self, first_name, last_name, phone_number, reg_id):
        try:
            user_data = Users(first_name=first_name,
                              last_name=last_name,
                              phone_number=phone_number,
                              registration_id=reg_id,
                              uuid=generate_uuid())
            Users.save_db(user_data)
            if user_data.id is None:
                raise SQLAlchemyError('User data not inserted')
            return user_data.id, user_data.uuid
        except SQLAlchemyError as error:
            db.session.rollback()
            raise InternalServerError(str(error))

    def update_user_byid(self, id, first_name, last_name, phone_number):
        try:
            exist_user = self.commonObj.check_user_exist(id)
            exist_user.first_name = first_name
            exist_user.last_name = last_name
            exist_user.phone_number = phone_number
            Users.update_db(exist_user)
        except (TypeError, AttributeError) as error:
            raise InternalServerError(str(error))

    def list_users(self):
        try:
            users_list = db.session.query(Users).Join().all()
            users_data = [{'id': user.id,
                           'first_name': user.first_name,
                           'last_name': user.last_name}
                          for user in users_list]
            return users_data
        except SQLAlchemyError as error:
            db.session.rollback()
            raise InternalServerError(error)

    def delete_user_byid(self, user_id):
        self.commonObj.check_user_exist(user_id)
        try:
            user = db.session.query(Users).filter_by(id=user_id).first()
            if user is None:
                raise NotFound('user does not exist')
            Users.delete_obj(user)
        except SQLAlchemyError as error:
            db.session.rollback()
            raise InternalServerError(error)

    def assign_user_role(self, user_id):
        try:
            self.commonObj.check_user_exist(user_id)
            user_role = UserRoles(role_id=4, user_id=user_id)
            UserRoles.save_db(user_role)
            if user_role.id is None:
                raise SQLAlchemyError('Roles not updated')
        except SQLAlchemyError as error:
            raise InternalServerError(str(error))
