import os

from config import read_environ_value

SERIAL_NUMBER_LENGTH = 8
ENCRYPTION_KEY_LENGTH = 16
ADMIN = "ADMIN"
ESUSER = "USER"
PROVIDER = "PROVIDER"
PATIENT = "PATIENT"
DEVICE_STATUS = "Assigned"
value = os.environ.get("SECRET_MANAGER_ARN")
REPORT_BUCKET_NAME = read_environ_value(value, "REPORT_BUCKET_NAME")
DEVICE_BASE_URL = os.getenv("DEVICE_BASE_URL")
CHECK_DEVICE_EXIST_URL = DEVICE_BASE_URL + "/device/exists"
GET_DEVICE_DETAIL_URL = DEVICE_BASE_URL + "/device"
UPDATE_DEVICE_STATUS_URL = DEVICE_BASE_URL + "/update/device/status"
GET_DEVICE_STATUS_URL = DEVICE_BASE_URL + "/get/device/status"
LOGIN_URL = DEVICE_BASE_URL + "/login"

# Device Metrics constants
DEVICE_BUTTON_PRESS = "buttonPresses"
DEVICE_PATCH_BATTERY_VOLTS = "patchBattVolts"
DEVICE_AUX_BATTERY_VOLTS = "auxBattVolts"
DEVICE_ROLLING_MEAN_32 = "rollingMean32"
DEVICE_ROLLING_MEAN_100 = "rollingMean100"
DEVICE_METRICS_TIMESTAMP = "timestamp"
