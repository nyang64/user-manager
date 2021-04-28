from model.roles import Roles
from model.users import Users
from schema.user_roles_schema import UserRolesSchema
from seeds import users
from seeds.helpers import message_details, print_message_details
from seeds.seed_data import ADMIN_USER

user_role_schema = UserRolesSchema()


def seed():
    create_admin()


def create_admin():
    registered_user_id = users.create_and_register_user(ADMIN_USER)
    admin = Users.find_by_id(registered_user_id)

    role = Roles.find_by_name("ADMIN")
    admin_role = user_role_schema.load({"user_id": admin.id, "role_id": role.id})
    admin_role.save_to_db()

    message_details[
        "admin"
    ] += f"Admin with id '{admin.id}' created and role id {role.id}"
    print_message_details()

    return admin.id
