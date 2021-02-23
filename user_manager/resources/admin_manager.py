from model.user_registration import UserRegister
from model.users import Users
from model.roles import Roles
from model.address import Address
from utils.common import encPass
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import InternalServerError
from db import db
from model.facilities import Facilities
from services.repository.db_repositories import DbRepository
from services.user_services import UserServices
from services.auth_services import AuthServices
from utils.constants import ADMIN

db_obj = DbRepository()
auth_obj = AuthServices()
user_obj = UserServices()


class admin_manager():
    def __init__(self):
        pass

    def seed_db(self):
        role_msg = self.seed_roles()
        admin_msg = self.register_admin()
        address_msg, address_id = self.seed_address()
        facility_msg = self.seed_facility(address_id=address_id,
                                          name='facilitytest')
        return {'message': [role_msg, admin_msg,
                            address_msg, facility_msg]}, 201

    def register_admin(self):
        admin_json = {
            'first_name':'admin',
            'last_name':'admin',
            'phone_number':'8097810754',
            'uuid':'1212121212',
            'email':'admin@elementsci.com',
            'password':'admin123'
        }
        if admin_json is False:
            return {"message": " Not created"}, 400
        exist = user_exists(admin_json)
        if exist is False:
            return 'Admin already created'
        insert_ref(admin_json)
        return 'Admin Created'

    def seed_roles(self):
        roles = db.session.query(Roles).all()
        if len(roles) > 3:
            return 'Role exist'
        role_list = ['ADMIN', 'PROVIDER', 'PATIENT', 'USER']
        roles = [Roles(role_name=role) for role in role_list]
        db.session.add_all(roles)
        db.session.commit()
        return 'Role Created'

    def seed_address(self):
        address_id = save_address(None, None, None, None,
                                  None, None, None)
        return 'Address Added', address_id

    def seed_facility(self, address_id, name):
        save_facility(address_id, name)
        return 'Facility Added'


def save_facility(address_id, name):
    try:
        facility_data = Facilities(address_id=address_id, name=name)
        db_obj.save_db(facility_data)
        return facility_data.id
    except SQLAlchemyError as error:
        db.session.rollback()
        raise InternalServerError(str(error))


def save_address(user_id, street_address_1,
                 street_address_2, city, state, country, postal_code):
    try:
        address_data = Address(
            user_id=user_id,
            street_address_1=street_address_1,
            street_address_2=street_address_2,
            city=city,
            state=state,
            country=country,
            postal_code=postal_code
            )
        db_obj.save_db(address_data)
        return address_data.id
    except SQLAlchemyError as error:
        db.session.rollback()
        raise InternalServerError(str(error))


def user_exists(provider_json):
    user_reg_data = UserRegister.find_by_email(
        email=provider_json['email']
            )
    if user_reg_data is not None:
        if (Users.find_by_registration_id(
            registration_id=user_reg_data.id
                ) is not None):
            return False
    if user_reg_data is not None:
        return False



def insert_ref(provider_json):
    try:
        register = (str(provider_json['email']).lower(), encPass(provider_json['password']))
        user = (provider_json['first_name'], provider_json['last_name'],
                provider_json['phone_number'])
        reg_id = auth_obj.register_new_user(register)
        user_id, uuid = user_obj.save_user(user[0], user[1], user[2], reg_id)
        user_obj.assign_role(user_id, ADMIN)
        db_obj.commit_db()
    except SQLAlchemyError as error:
        raise InternalServerError(str(error))
    except (AttributeError, NameError, TypeError) as e:
        raise InternalServerError(str(e))
    return user_id
