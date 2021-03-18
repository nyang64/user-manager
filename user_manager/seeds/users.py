from model.user_registration import UserRegister
from seeds.helpers import print_message_details
from services.user_services import UserServices
from services.auth_services import AuthServices

from utils.constants import ADMIN

message_details = {
    "registration": ""
}

auth_obj = AuthServices()
user_obj = UserServices()


def registration_exists(user_email):
    return UserRegister.find_by_email(user_email)


def create_and_register_user(user_details):
    if registration_exists(user_details["register"]["email"]):
        message_details["registration"] += "Registration already exists. Did not create user."
        print_message_details()

    else:
        reg_id = auth_obj.register_new_user(user_details["register"]["email"],
                                            user_details["register"]["password"])
        user_id, uuid = user_obj.save_user(user_details["user"]["first_name"],
                                           user_details["user"]["last_name"],
                                           user_details["user"]["phone_number"],
                                           reg_id)
        user_obj.assign_role(user_id, ADMIN)
        message_details["registration"] += f"Registration with id {reg_id} created."
        print_message_details()

        return user_id
