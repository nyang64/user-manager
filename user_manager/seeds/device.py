from model.device_metric_type import DeviceMetricType
from model.device_ui_status_type import DeviceUiStatusType
from seeds.helpers import print_message_details, message_details
from utils import constants

def seed():
    device_metrics_types()
    device_status_types()


def device_metrics_types():
    print("Device metrics seed")
    data_from_db = DeviceMetricType.all()

    if len(data_from_db) > 0:
        message_details["metric_types"] = "Nothing was added some metrics already exist. "
    else:
        metrics_types = [constants.DEVICE_AUX_BATTERY_VOLTS,
                      constants.DEVICE_PATCH_BATTERY_VOLTS,
                      constants.DEVICE_ROLLING_MEAN_32,
                      constants.DEVICE_BUTTON_PRESS,
                      constants.DEVICE_ROLLING_MEAN_100,
                      constants.DEVICE_METRICS_TIMESTAMP]
        for name in metrics_types:
            metrics_type = DeviceMetricType(name=name)
            metrics_type.save_to_db()
            message_details["metrics types"] = "Metrics types were created"

    print_message_details()


# These are the known UI status that are sent from the device for ES2.
DEVICE_STATUS_TYPES = {
    "12": "NOTIF_STATUS_MONITOR_ENTRY",
    "13": "NOTIF_STATUS_ERA",
    "15": "NOTIF_STATUS_MEDIUM_PRIORITY_MRA",
    "19": "NOTIF_STATUS_HIGH_PRIORITY_MRA",
    "21": "NOTIF_STATUS_DEVICE_IN_STANDBY",
    "23": "NOTIF_STATUS_TREATMENT_DELAYED",
    "29": "", #Could not find the status type
    "33": "NOTIF_STATUS_APPLICATION_ENTRY",
    "42": "NOTIF_STATUS_APPLICATION_REMOVAL",
    "47": "NOTIF_STATUS_TREATMENT_DELIVERED_NO_MRA",
    "55": "NOTIF_STATUS_PATCHES_DISABLED" ,
    "59": "NOTIF_STATUS_DEVICE_IN_STANDBY",
    "69": "NOTIF_STATUS_APPLICATION_EXIT_TO_SHIPPING",
    "72": "NOTIF_STATUS_EMERGENCY_SERVICE",
    "74": "NOTIF_STATUS_REMOVAL_EXIT_TO_SHIPPING",
    "76": "NOTIF_STATUS_TREATMENT_DELIVERED_MRA",
    "79": "NOTIF_STATUS_PRESS_DOWN_DEVICE",
    "81": "NOTIF_STATUS_DEVICE_OFF_BODY",
    "85": "NOTIF_STATUS_EMERGENCY_SERVICE",
    "87": "NOTIF_STATUS_TREATMENT_DELIVERED_MRA",
    "92": "NOTIF_STATUS_MONITOR_ENTRY_AFTER_OFF_BODY",
    "102": "NOTIF_STATUS_BLE_PAIRING_SUCCESS",
    "107": "NOTIF_STATUS_EMI",
    "109": "NOTIF_STATUS_M4_DISCONNECT",
    "111": "NOTIF_STATUS_M1_DISCONNECT",
    "113": "NOTIF_STATUS_NO_THERAPY_MRA_HIGH",
    "116": "NOTIF_STATUS_DEVICE_REMOVAL_NO_THERAPY_REPLACE_DEV",
    "118": "NOTIF_STATUS_REMOVAL_EXIT_TO_SHIPPING_DEFIB",
    "E1": "DEVICE_DISCONNECTED_PENDING",
    "E2": "DEVICE_DISCONNECTED",
    "E3": "DEVICE_CONNECTION_ERROR",
    "E4": "NETWORK_UNAVAILABLE",
    "E5": "UNABLE_TO_TRANSMIT",
    "E6": "BLUETOOTH_DISABLED",
    "E7": "BLUETOOTH_DISALLOWED",
    "E8": "UNKNOWN_SERIAL_NUMBER",
}
def device_status_types():
    print("Device Status types seed")
    data_from_db = DeviceUiStatusType.all()

    if len(data_from_db) > 0:
        message_details["device_status_types"] = "Nothing was added some metrics already exist. "
    else:
        for key, value in DEVICE_STATUS_TYPES.items():
            status_type = DeviceUiStatusType(name=value, ui_id=key)
            status_type.save_to_db()
            message_details["Device ui status types"] = "Status types were created"

    print_message_details()

