import os
from config import read_environ_value
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
