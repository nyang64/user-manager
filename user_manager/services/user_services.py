import logging

from db import db
from model.roles import Roles
from model.user_roles import UserRoles
from model.user_status import UserStatus
from model.user_status_type import UserStatusType
from model.users import Users
from services.auth_services import AuthServices
from services.repository.db_repositories import DbRepository
from sqlalchemy.exc import SQLAlchemyError
from utils.common import generate_uuid
from utils.constants import ENROLLED
from werkzeug.exceptions import InternalServerError, NotFound


class UserServices(DbRepository):
    def __init__(self):
        self.auth_obj = AuthServices()

    def register_user(self, register, user):
        reg_id = self.auth_obj.register_new_user(register[0], register[1])
        user_id, user_uuid = self.save_user(user[0], user[1], user[2], reg_id)

        self.assign_role(user_id, role_name=user[3])
        self.assign_status(user_id)
        self.commit_db()

        return user_id, user_uuid

    def save_user(self, first_name, last_name, phone_number, reg_id):
        user_data = Users(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            registration_id=reg_id,
            uuid=generate_uuid(),
        )
        self.flush_db(user_data)

        return user_data.id, user_data.uuid

    def update_user_byid(self, user_id, first_name, last_name, phone_number):
        try:
            exist_user = Users.check_user_exist(user_id)
            if bool(exist_user) is False:
                raise NotFound("user does not exist")
            exist_user.first_name = first_name
            exist_user.last_name = last_name
            exist_user.phone_number = phone_number
            self.update_db(exist_user)
        except (TypeError, AttributeError) as error:
            logging.error(error)
            raise InternalServerError(str(error))

    def list_users(self):
        try:
            users_list = db.session.query(Users).Join().all()
            users_data = [
                {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                }
                for user in users_list
            ]
            return users_data
        except SQLAlchemyError as error:
            logging.error(error)
            raise InternalServerError(error)

    def delete_user_byid(self, user_id):
        exist_user = Users.check_user_exist(user_id)
        if bool(exist_user) is False:
            raise NotFound("user does not exist")
        self.auth_obj.delete_regtration(exist_user.registration_id)

    def assign_role(self, user_id, role_name="PATIENT"):
        role_id = Roles.get_roleid(role_name)
        user_role = UserRoles(role_id=role_id.id, user_id=user_id)
        self.flush_db(user_role)
        return user_role.role

    def get_detail_by_email(self, email):
        """ Get the detail of logged in user by email id"""
        from model.user_registration import UserRegister

        try:
            exist_registration = UserRegister.find_by_email(email)
            if exist_registration is None:
                raise NotFound(f"{email} not found")
            user = (
                db.session.query(Users.id, Users.uuid, UserRegister.id)
                .filter(UserRegister.id == Users.registration_id)
                .filter(UserRegister.email == email)
                .first()
            )
            if user is None:
                raise NotFound("user detail not found")
            return user
        except SQLAlchemyError as error:
            logging.error(str(error))
            raise InternalServerError(str(error))

    @classmethod
    def get_user_by_registration_id(self, user_reg_id) -> "Users":
        try:
            user_data = Users.find_by_registration_id(registration_id=user_reg_id)
            if user_data is None:
                raise NotFound("User Details Not Found")
            return user_data
        except Exception as error:
            logging.error(str(error))
            raise InternalServerError("Something Went Wrong")

    @classmethod
    def get_user_by_user_id(cls, user_id) -> "Users":
        try:
            user_data = Users.find_by_id(_id=user_id)
            if user_data is None:
                raise NotFound("User Details Not Found")
            return user_data
        except Exception as error:
            logging.error(str(error))
            raise InternalServerError("Something Went Wrong")

    def assign_status(self, user_id):
        status_type = UserStatusType.find_by_name(ENROLLED)
        user_status = UserStatus(status_id=status_type.id, user_id=user_id)

        self.flush_db(user_status)

        return user_status.status
