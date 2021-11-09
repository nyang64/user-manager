from model.provider_role_types import ProviderRoleTypes
from model.roles import Roles
from seeds.helpers import print_message_details, message_details
from schema.provider_role_types_schema import ProviderRoleTypesSchema
from utils.constants import OUTPATIENT_PROVIDER, PRESCRIBING_PROVIDER, STUDY_COORDINATOR



def seed():
    user()
    provider()


def provider():
    existing_provider_roles = ProviderRoleTypes.all()

    provider_roles = [{"name": OUTPATIENT_PROVIDER},
            {"name": PRESCRIBING_PROVIDER},
            {"name": STUDY_COORDINATOR}]

    # Check if status_type exists
    if len(existing_provider_roles) > 0:
        # Iterate through dictionary and see if exists
        for item in provider_roles:
            for key, value in item.items():
                if not ProviderRoleTypes.find_by_name(_name=value):
                    new_role_type = ProviderRoleTypes(name=value)
                    new_role_type.save_to_db()
                    message_details["Provider Role Type"] = "Provider Role Type was created"
            message_details["Provider Role Type"] = "Nothing else was added some roles already exist. "
    else:
        for item in provider_roles:
            for key, value in item.items():
                status_type = ProviderRoleTypes(name=value)
                status_type.save_to_db()
                message_details["Provider Role types"] = "Role types was created"

    print_message_details()


def user():
    roles = Roles.all()
    roles_list = ["ADMIN", "PROVIDER", "PATIENT", "USER", "CUSTOMER_SERVICE", "STUDY_MANAGER", "SITE_COORDINATOR"]

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

