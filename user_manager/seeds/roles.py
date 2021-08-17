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
    roles_list = ["ADMIN", "PROVIDER", "PATIENT", "USER", "CUSTOMER_SERVICE", "STUDY_MANAGER"]

    if len(roles) > 0:
        # Iterate through dictionary and see if exists
        for value in roles_list:
            print(value)
            if not Roles.find_by_name(value):
                message_details["Roles"] = "Added a new role " + value
                new_role = Roles(role_name=value)
                new_role.save_to_db()
                message_details["Role types"] = "Role type was created"
    else:
        for value in roles_list:
            new_role = Roles(role_name=value)
            new_role.save_to_db()
            message_details["Device ui status types"] = "Added a new role " + value

