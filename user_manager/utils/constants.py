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
CHECK_DEVICE_EXIST_URL = read_environ_value(value, "CHECK_DEVICE_EXIST_URL")
GET_DEVICE_DETAIL_URL = read_environ_value(value, "GET_DEVICE_DETAIL_URL")
GET_DEVICE_STATUS_URL = read_environ_value(value, "GET_DEVICE_STATUS_URL")
UPDATE_DEVICE_STATUS_URL = read_environ_value(value, "UPDATE_DEVICE_STATUS_URL")
PROVIDER_OUTPATIENT = {
    "user": {
        "first_name": "alexx",
        "last_name": "brandao",
        "phone_number": "2223332222",
        "type": PROVIDER
    },
    "register": {
        "email": "alexxxhdi123d45fc6d7@elementsci.com",
        "password": "ilovealmonds"
    },
    "provider": {
        "facility": {
            "name": "The Healthiest Heart Hospital",
            "address": {
                "street_address_1": "sunset blvd",
                "street_address_2": "unit 192",
                "city": "San Francisco",
                "state": "CA",
                "country": "USA",
                "postal_code": 94103
            }
        },
        "type": "outpatient"
    }
}

PROVIDER_PRESCRIBING = {
    "user": {
        "first_name": "jyothii",
        "last_name": "jayaraman",
        "phone_number": "1112223333",
        "type": PROVIDER
    },
    "register": {
        "email": "jyothiciiiidhi1d2fd56@elementsci.com",
        "password": "ilovealmonds"
    },
    "provider": {
        "facility": {
            "name": "The Healthiest Heart Hospital",
            "address": {
                "street_address_1": "sunset blvd",
                "street_address_2": "unit 192",
                "city": "San Francisco",
                "state": "CA",
                "country": "USA",
                "postal_code": 94103
            }
        },
        "type": "prescribing"
    }
}
PATIENT_1_DICTIONARY = {
    "user": {
        "first_name": "mattheww",
        "last_name": "serna ruiz",
        "phone_number": "4445556666",
        "type": PATIENT
    },
    "register": {
        "email": "matthewwwwhdi12@elementsci.com",
        "password": "darjikittycat"
    },
    "patient": {
        "emergency_contact_name": "Darji",
        "emergency_contact_phone": "3335554444",
        "date_of_birth": datetime(1956, 5, 17).isoformat()
    }
}

PATIENT_2_DICTIONARY = {
    "user": {
        "first_name": "lauraa",
        "last_name": "kirby",
        "phone_number": "7778889999",
        "type": PATIENT
    },
    "register": {
        "email": "lauraaaadhi12@elementsci.com",
        "password": "rosiepupdog"
    },
    "patient": {
        "emergency_contact_name": "Darji",
        "emergency_contact_phone": "33366655555",
        "date_of_birth": datetime(1946, 1, 26).isoformat()
    }
}

ADMIN_USER = {
    "user": {
        "first_name": "admin",
        "last_name": "admin",
        "phone_number": "8097810754",
        "type": PROVIDER
    },
    "register": {
        "email": "piggieehi12@elementsci.com",
        "password": read_environ_value(value, "ADMIN_PASSWORD")
    }
}

PATIENTS = [PATIENT_1_DICTIONARY, PATIENT_2_DICTIONARY]
