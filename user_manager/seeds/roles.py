from model.provider_role_types import ProviderRoleTypes
from model.roles import Roles
from seeds.helpers import print_message_details, message_details
from schema.provider_role_types_schema import ProviderRoleTypesSchema


def seed():
    user()
    provider()


def provider():
    existing_provider_roles = ProviderRoleTypes.all()

    if len(existing_provider_roles) >= 2:
        message_details["provider_roles"] += f"Provider roles not added because 2 already exist. "
    else:
        provider_roles = [{"name": "outpatient"}, {"name": "prescribing"}]

        for role in provider_roles:
            provider_role_type_schema = ProviderRoleTypesSchema()
            provider_role = provider_role_type_schema.load(role)
            provider_role.save_to_db()
            message_details["provider_roles"] += f"Provider role: {role['name']} was added. "

    print_message_details()


def user():
    roles = Roles.all()

    if len(roles) > 3:
        message_details["user_roles"] = "Nothing was added because 3 roles already exist. "
    else:
        role_names = ['ADMIN', 'PROVIDER', 'PATIENT', 'USER']
        for name in role_names:
            new_role = Roles(role_name=name)
            new_role.save_to_db()
            message_details["user_roles"] = "Roles were created"

    print_message_details()
