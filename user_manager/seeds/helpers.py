import json

message_details = {
    "patient": "",
    "provider": "",
    "admin_user": "",
    "address": "",
    "registration": "",
    "facility": "",
    "provider_roles": "",
    "user_roles": "",
    "admin": ""
}


def print_message_details():
    print(json.dumps(message_details, indent=4))
