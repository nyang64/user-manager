from model.user_registration import UserRegister
from model.users import Users
from seeds.helpers import message_details, print_message_details
from services.auth_services import AuthServices
from services.user_services import UserServices

auth_obj = AuthServices()
user_obj = UserServices()


def registration_exists(user_email):
    return UserRegister.find_by_email(user_email)


def create_and_register_user(user_details):
    # Returns reg obj
    exists = registration_exists(user_details["register"]["email"])

    if exists:
        message_details[
            "registration"
        ] += "Registration already exists. Did not create user."
        print_message_details()
        user = Users.find_by_registration_id(registration_id=exists.id)
        return user.id
    else:
        registration_details = [
            user_details["register"]["email"],
            user_details["register"]["password"],
        ]
        user_details = [
            user_details["user"]["first_name"],
            user_details["user"]["last_name"],
            user_details["user"]["phone_number"],
            user_details["user"]["role_name"],
            user_details["user"]["external_user_id"]
        ]
        user_id, user_uuid = user_obj.register_user(registration_details, user_details)
        user = Users.find_by_id(user_id)
        message_details[
            "registration"
        ] += f"Registration with id {user.registration_id} created."
        message_details["user"] += f"User with id {user.id} created."

        print_message_details()

        return user_id
