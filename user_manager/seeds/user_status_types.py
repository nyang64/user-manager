from model.user_status_type import UserStatusType
from schema.user_status_type_schema import UserStatusTypeSchema
from seeds.helpers import message_details, print_message_details
from utils.constants import ACTIVE, DISABLED, DISENROLLED, ENROLLED, SUSPENDED


def seed():
    user_status_types()


def user_status_types():
    existing_provider_roles = UserStatusType.all()
    status_types = [
        {"name": DISABLED},
        {"name": ACTIVE},
        {"name": SUSPENDED},
        {"name": ENROLLED},
        {"name": DISENROLLED},
    ]

    type_count = len(status_types)

    if len(existing_provider_roles) >= type_count:
        message_details[
            "user_status_types"
        ] += f"UserStatusTypes were not added because {type_count} already exist."
    else:
        message_details["user_status_types"] += "UserStatusTypes added: "
        for status_type in status_types:
            user_status_type_schema = UserStatusTypeSchema()
            provider_role = user_status_type_schema.load(status_type)
            provider_role.save_to_db()
            message_details["user_status_types"] += f"{status_type['name']}"

    print_message_details()
