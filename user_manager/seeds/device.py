from model.device_metric_type import DeviceMetricType
from seeds.helpers import print_message_details, message_details
from utils import constants

def seed():
    device_metrics_types()

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