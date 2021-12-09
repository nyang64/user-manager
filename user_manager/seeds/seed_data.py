import os
from datetime import datetime

from config import read_environ_value
from utils.constants import ADMIN, FLASK_ENV, PATIENT, PROVIDER, STUDY_MANAGER, CUSTOMER_SERVICE

value = os.getenv("SECRET_MANAGER_ARN")

APPLE_USER = {
    "user": {
        "first_name": "Apple",
        "last_name": "Inc",
        "phone_number": "4445556666",
        "role_name": PATIENT,
    },
    "register": {"email": "sw-eng@elementsci.com", "password": "ThankYou123"},
    "patient": {
        "emergency_contact_name": "Google",
        "emergency_contact_phone": "6663339999",
        "date_of_birth": datetime(1990, 6, 25).isoformat(),
        "gender": "non-binary",
        "indication": "E/F",
    },
    "address": {
        "street_address_1": "1 Apple Park Way",
        "street_address_2": "",
        "city": "Cupertino",
        "state": "CA",
        "country": "USA",
        "postal_code": "95014",
    },
}

PROVIDER_PRESCRIBING = {
    "user": {
        "first_name": "Zubin",
        "last_name": "Eapen",
        "phone_number": "1112223333",
        "role_name": PROVIDER,
    },
    "register": {
        "email": read_environ_value(value, "PROVIDER_EMAIL_ONE"),
        "password": read_environ_value(value, "PROVIDER_PASSWORD"),
    },
    "provider": {
        "facility": {
            "name": "Smiling Heart Hospital",
            "on_call_phone": "8883339999",
            "address": {
                "street_address_1": "Arguello Blvd",
                "street_address_2": "",
                "city": "San Francisco",
                "state": "CA",
                "country": "USA",
                "postal_code": "94118",
            },
        },
        "role_name": "prescribing",
    },
}

PROVIDER_OUTPATIENT = {
    "user": {
        "first_name": "Kiran",
        "last_name": "Mathews",
        "phone_number": "3332226666",
        "role_name": PROVIDER,
    },
    "register": {
        "email": read_environ_value(value, "PROVIDER_EMAIL_TWO"),
        "password": read_environ_value(value, "PROVIDER_PASSWORD"),
    },
    "provider": {
        "facility": {
            "name": "Healthy Hearts",
            "on_call_phone": "5556667777",
            "external_facility_id": "101",
            "address": {
                "street_address_1": "Market St",
                "street_address_2": "",
                "city": "San Francisco",
                "state": "CA",
                "country": "USA",
                "postal_code": "94107",
            },
        },
        "role_name": "outpatient",
        "external_user_id": "101-102"
    },
}

PROVIDER_OUTPATIENT_2 = {
    "user": {
        "first_name": "Alex",
        "last_name": "Brandao",
        "phone_number": "2223332222",
        "role_name": PROVIDER,
    },
    "register": {
        "email": read_environ_value(value, "PROVIDER_EMAIL_DEV"),
        "password": read_environ_value(value, "SEED_PASSWORD"),
    },
    "provider": {
        "facility": {
            "name": "Happy Heart",
            "on_call_phone": "5554443333",
            "external_facility_id": "102",
            "address": {
                "street_address_1": "Townsend St.",
                "street_address_2": "",
                "city": "San Francisco",
                "state": "CA",
                "country": "USA",
                "postal_code": "94103",
            },
        },
        "role_name": "outpatient",
        "external_user_id": "101-102"
    },
}

PATIENT_1_DICTIONARY = {
    "user": {
        "first_name": "Matthew",
        "last_name": "Serna",
        "phone_number": "4445556666",
        "role_name": PATIENT,
    },
    "register": {
        "email": read_environ_value(value, "PATIENT_EMAIL_ONE_DEV"),
        "password": read_environ_value(value, "SEED_PASSWORD"),
    },
    "patient": {
        "emergency_contact_name": "Darji",
        "emergency_contact_phone": "3335554444",
        "date_of_birth": datetime(1956, 5, 17).isoformat(),
        "gender": "male",
        "indication": "A/B",
    },
    "address": {
        "street_address_1": "Dolores St",
        "street_address_2": "",
        "city": "San Francisco",
        "state": "CA",
        "country": "USA",
        "postal_code": "94103",
    },
}

PATIENT_2_DICTIONARY = {
    "user": {
        "first_name": "Laura",
        "last_name": "Kirby",
        "phone_number": "7778889999",
        "role_name": PATIENT,
    },
    "register": {
        "email": read_environ_value(value, "PATIENT_EMAIL_TWO_DEV"),
        "password": read_environ_value(value, "SEED_PASSWORD"),
    },
    "patient": {
        "emergency_contact_name": "Rosie",
        "emergency_contact_phone": "33366655555",
        "date_of_birth": datetime(1946, 1, 26).isoformat(),
        "gender": "female",
        "indication": "C/D",
    },
    "address": {
        "street_address_1": "Market St",
        "street_address_2": "",
        "city": "San Francisco",
        "state": "CA",
        "country": "USA",
        "postal_code": "94103",
    },
}

ADMIN_USER = {
    "user": {
        "first_name": "admin",
        "last_name": "admin",
        "phone_number": "8097810754",
        "role_name": ADMIN,
        "external_user_id": "000-00"
    },
    "register": {
        "email": read_environ_value(value, "ADMIN_USERNAME"),
        "password": read_environ_value(value, "ADMIN_PASSWORD"),
    },
}

STUDY_MANAGER = {
    "user": {
        "first_name": "ES",
        "last_name": "StudyMgr",
        "phone_number": "4158726500",
        "role_name": STUDY_MANAGER,
        "external_user_id": "000-00"
    },
    "register": {
        "email": read_environ_value(value, "STUDY_MANAGER_USERNAME"),
        "password": read_environ_value(value, "STUDY_MANAGER_PASSWORD"),
    },
}

CUSTOMER_SERVICE = {
    "user": {
        "first_name": "ES",
        "last_name": "CustomerService",
        "phone_number": "4158726500",
        "role_name": CUSTOMER_SERVICE,
        "external_user_id": "000-00"
    },
    "register": {
        "email": read_environ_value(value, "CUSTOMER_SERVICE_EMAIL"),
        "password": read_environ_value(value, "CUSTOMER_SERVICE_PASSWORD"),
    },
}


PATIENTS = [PATIENT_1_DICTIONARY, PATIENT_2_DICTIONARY, APPLE_USER]
