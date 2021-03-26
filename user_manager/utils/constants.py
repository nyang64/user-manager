from config import read_environ_value
import os
from datetime import datetime

SERIAL_NUMBER_LENGTH = 8
ENCRYPTION_KEY_LENGTH = 16
ADMIN = 'ADMIN'
ESUSER = 'USER'
PROVIDER = 'PROVIDER'
PATIENT = 'PATIENT'
DEVICE_STATUS = 'Assigned'
value = os.environ.get('user-manager-secrets')
REPORT_BUCKET_NAME = read_environ_value(value, "REPORT_BUCKET_NAME")
secrets_manager_data = os.environ.get('user-manager-secrets')

DEVICE_BASE_URL = os.environ.get("DEVICE_BASE_URL")
CHECK_DEVICE_EXIST_URL = DEVICE_BASE_URL + '/device/exists'
GET_DEVICE_DETAIL_URL = DEVICE_BASE_URL + '/device'
UPDATE_DEVICE_STATUS_URL = DEVICE_BASE_URL + '/update/device/status'
GET_DEVICE_STATUS_URL = DEVICE_BASE_URL + '/get/device/status'
LOGIN_URL = DEVICE_BASE_URL + '/login'

REPORT_BUCKET_NAME = read_environ_value(secrets_manager_data, "REPORT_BUCKET_NAME")

ADMIN_EMAIL = read_environ_value(secrets_manager_data, "ADMIN_USERNAME")
ADMIN_PASSWORD = read_environ_value(secrets_manager_data, "ADMIN_PASSWORD")

PROVIDER_OUTPATIENT = {
    "user": {
        "first_name": "Alex",
        "last_name": "Brandao",
        "phone_number": "2223332222",
        "type": PROVIDER
    },
    "register": {
        "email": "alex@elementsci.com",
        "password": "ilovealmonds"
    },
    "provider": {
        "facility": {
            "name": "Happy Heart",
            "on_call_phone": "8883339999",
            "address": {
                "street_address_1": "Townsend St.",
                "street_address_2": "",
                "city": "San Francisco",
                "state": "CA",
                "country": "USA",
                "postal_code": "94103"
            }
        },
        "type": "outpatient"
    }
}

PROVIDER_PRESCRIBING = {
    "user": {
        "first_name": "Jyothii",
        "last_name": "Jayaraman",
        "phone_number": "1112223333",
        "type": PROVIDER
    },
    "register": {
        "email": "jyothii@elementsci.com",
        "password": "ilovealmonds"
    },
    "provider": {
        "facility": {
            "name": "Heart Hospital",
            "on_call_phone": "8883339999",
            "address": {
                "street_address_1": "Arguello Blvd",
                "street_address_2": "",
                "city": "San Francisco",
                "state": "CA",
                "country": "USA",
                "postal_code": "94103"
            }
        },
        "type": "prescribing"
    }
}
PATIENT_1_DICTIONARY = {
    "user": {
        "first_name": "Matthew",
        "last_name": "Serna",
        "phone_number": "4445556666",
        "type": PATIENT
    },
    "register": {
        "email": "matthew@elementsci.com",
        "password": "ilovealmonds"
    },
    "patient": {
        "emergency_contact_name": "Darji",
        "emergency_contact_phone": "3335554444",
        "date_of_birth": datetime(1956, 5, 17).isoformat(),
        "gender": "male"
    },
    "address": {
        "street_address_1": "Dolores St",
        "street_address_2": "",
        "city": "San Francisco",
        "state": "CA",
        "country": "USA",
        "postal_code": "94103"
    }
}

PATIENT_2_DICTIONARY = {
    "user": {
        "first_name": "Laura",
        "last_name": "Kirby",
        "phone_number": "7778889999",
        "type": PATIENT
    },
    "register": {
        "email": "laura@elementsci.com",
        "password": "ilovealmonds"
    },
    "patient": {
        "emergency_contact_name": "Rosie",
        "emergency_contact_phone": "33366655555",
        "date_of_birth": datetime(1946, 1, 26).isoformat(),
        "gender": "female"
    },
    "address": {
        "street_address_1": "Market St",
        "street_address_2": "",
        "city": "San Francisco",
        "state": "CA",
        "country": "USA",
        "postal_code": "94103"
    }
}

ADMIN_USER = {
    "user": {
        "first_name": "admin",
        "last_name": "admin",
        "phone_number": "8097810754",
        "type": ADMIN
    },
    "register": {
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    }
}

PATIENTS = [PATIENT_1_DICTIONARY, PATIENT_2_DICTIONARY]
