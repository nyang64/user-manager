import json
import logging

from db import db
from model.roles import Roles
from model.user_roles import UserRoles
from model.user_status import UserStatus
from model.address import Address
from model.user_status_type import UserStatusType
from model.users import Users
from model.study_managers import StudyManagers
from services.auth_services import AuthServices
from services.repository.db_repositories import DbRepository
from sqlalchemy.exc import SQLAlchemyError
from utils.common import generate_uuid
from utils.constants import ENROLLED, DISENROLLED, STUDY_MANAGER
from werkzeug.exceptions import InternalServerError, NotFound


class UserServices(DbRepository):
    def __init__(self):
        self.auth_obj = AuthServices()

    def register_user(self, register, user):
        reg_id = self.auth_obj.register_new_user(register[0], register[1])
        user_id, user_uuid = self.save_user(first_name=user[0],
                                            last_name=user[1],
                                            phone_number=user[2],
                                            external_user_id=user[4],
                                            reg_id=reg_id)

        self.assign_role(user_id, role_name=user[3])

        # check the role name
        if user[3] == STUDY_MANAGER:
            self.__register_study_manager(user_id, user)

        self.change_user_status(user_id, ENROLLED, "", "", None)
        self.commit_db()

        return user_id, user_uuid

    def save_user(self, first_name, last_name, phone_number, external_user_id, reg_id):
        user_data = Users(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            registration_id=reg_id,
            uuid=generate_uuid(),
            external_user_id=external_user_id
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

    def get_users_by_role(self, role_name):
        if role_name == STUDY_MANAGER:
            return self.__get_study_managers()


    def __get_study_managers(self):
        study_managers = db.session.query(Users, StudyManagers, Address) \
            .join(Users, StudyManagers.user_id == Users.id) \
            .join(Address, Address.id == StudyManagers.address_id).distinct(Users.id).all()

        users_list = []
        if study_managers is None or len(study_managers) == 0:
            return users_list, 0

        for x in study_managers:
            address = x[2]
            address_json = {}
            address_json["street_address_1"] = address.street_address_1
            address_json["street_address_2"] = address.street_address_2
            address_json["city"] = address.city
            address_json["state"] = address.state
            address_json["country"] = address.country
            address_json["postal_code"] = address.postal_code

            user = x[0]
            users_dict = {}
            users_dict["address"] = address_json
            users_dict["user_id"] = user.id
            users_dict["first_name"] = user.first_name
            users_dict["last_name"] = user.last_name
            users_dict["phone_number"] = user.phone_number
            users_dict["email"] = user.registration.email

            users_list.append(users_dict)

        return users_list, len(study_managers)

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

    def delete_user_byid(self, user_id, reason, notes, session):
        exist_user = Users.check_user_exist(user_id)
        if bool(exist_user) is False:
            raise NotFound("user does not exist")
        session = self.auth_obj.delete_registration(exist_user.registration_id, session)
        session = self.change_user_status(user_id, DISENROLLED, reason, notes, session)

        return session

    def assign_role(self, user_id, role_name="PATIENT"):
        role_id = Roles.get_roleid(role_name)
        if role_id is None:
            raise Exception("role not found")

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

    def change_user_status(self, user_id, status, reason, notes, session):
        status_type = UserStatusType.find_by_name(status)

        # Update the existing status object. Do not add a new row.
        user_status_obj = UserStatus.get_user_status_by_user_id(user_id)

        if not user_status_obj:
            user_status_obj = UserStatus()
            user_status_obj.user_id = user_id

        user_status_obj.status_id = status_type.id
        user_status_obj.notes = notes
        user_status_obj.deactivation_reason = json.dumps(reason)

        if session:
            session.add(user_status_obj)
            return session
        else:
            self.flush_db(user_status_obj)
            return user_status_obj.id

    def __register_study_manager(self, user_id, user):
        sm = StudyManagers()
        sm.user_id = user_id

        # check if there is any address -
        # TODO We need to convert to an object instead of an array
        address = None
        if len(user) > 5:
            address = user[5]

        if address is not None:
            self.flush_db(address)
            sm.address_id = address.id

        self.flush_db(sm)

