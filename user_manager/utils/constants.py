import os

from config import read_environ_value

# -------------- AWS Secret Key -----------------
value = os.environ.get("SECRET_MANAGER_ARN")

# -------------- Environment Config -----------------
FLASK_ENV = read_environ_value(value, "FLASK_ENV")

# -------------- User -----------------
ADMIN = "ADMIN"
ESUSER = "USER"
PROVIDER = "PROVIDER"
PATIENT = "PATIENT"
DISABLED = "DISABLED"
ACTIVE = "ACTIVE"
SUSPENDED = "SUSPENDED"
ENROLLED = "ENROLLED"
DISENROLLED = "DISENROLLED"

# -------------- Report --------------
REPORT_BUCKET_NAME = read_environ_value(value, "REPORT_BUCKET_NAME")

# -------------- Device --------------
SERIAL_NUMBER_LENGTH = 8
ENCRYPTION_KEY_LENGTH = 16

# Device-manager url
DEVICE_BASE_URL = read_environ_value("DEVICE_BASE_URL")

# Statuses from device-manager
ASSIGNED = "Assigned"
AVAILABLE = "Available"

# Metrics
DEVICE_BUTTON_PRESS = "buttonPresses"
DEVICE_PATCH_BATTERY_VOLTS = "patchBattVolts"
DEVICE_AUX_BATTERY_VOLTS = "auxBattVolts"
DEVICE_ROLLING_MEAN_32 = "rollingMean32"
DEVICE_ROLLING_MEAN_100 = "rollingMean100"
DEVICE_METRICS_TIMESTAMP = "timestamp"

# Mock
DEVICE_INFO_MOCK = {
    "key": "32413046393134373030313234433230",
    "serial_number": "22222222",
}
FAKE_TOKEN = "12345ABCDEF"
