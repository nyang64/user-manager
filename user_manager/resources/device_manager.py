from flask import request

from model.device_metric_type import DeviceMetricType
from model.device_ui_status_type import DeviceUiStatusType
from schema.device_metric_schema import DeviceMetricSchema
from schema.device_metric_type_schema import DeviceMetricTypeSchema
from schema.device_ui_status_schema import DeviceUiStatusSchema
from schema.device_ui_status_type_schema import DeviceUiStatusTypeSchema
from services.device_manager_api import DeviceManagerApi
from utils.validation import validate_request
from utils.constants import PATIENT
from utils.jwt import require_user_token
from utils.device_utils import get_metrics_data, parse_metrics

import logging


class DeviceManager:
    def __init__(self):
        print('Init')

    @require_user_token(PATIENT)
    def create_status(self, decrypt):
        """
           Persist device UI status sent by the mobile app in the database.
           :param: None
           :return: Http response code with a message
        """
        logging.info('Saving device ui status')
        status_json = request.get_json()
        logging.info(status_json)
        statuses = status_json.get('statuses')

        for status in statuses:
            ui_status = {}
            ui_status['device_serial_number'] = status_json.get('device_serial_number')
            ui_status['receiver_recorded_at'] = status_json.get('received_at')
            ui_status['receiver_id'] = status_json.get('receiver_id')
            ui_status['recorded_at'] = status.get('recorded_at')
            status_type = DeviceUiStatusType.find_by_ui_id(status["ui_id"])

            if status_type is not None:
                ui_status["status_id"] = status_type.id
            else:
                logging.error("Could not find status type for {}".format(status["ui_id"]))

            status_schema = DeviceUiStatusSchema()
            status_model = status_schema.load(ui_status)
            status_model.save_to_db()

        return {"message": "Device ui status persisted"}, 201

    @require_user_token(PATIENT)
    def create_metric(self, decrypt):
        """
        Persist device metrics sent by the mobile app
        It is assumed that the token will be only the patient token.
        """
        logging.info('Persisting device metrics')
        metric_json = validate_request()
        logging.info(metric_json)

        device_serial_number = metric_json.get('device_serial_number')
        received_at = metric_json.get('received_at')
        receiver_id = metric_json.get('receiver_id')
        recorded_at = metric_json.get('recorded_at')
        device_metrics_hex = metric_json.get('device_metrics')

        if device_serial_number is None:
            logging.error("Missing serial number. Not able to process and persist the metrics")
            return {"message": "Missing device serial number"}, 400

        # Get the encryption key for the serial number
        encryption_key = DeviceManagerApi.get_device(device_serial_number).get("key")
        if encryption_key is None:
            logging.error("Could not find encryption key for thr serial number {}"
                          .format(device_serial_number))
            return {"message": "Missing encryption key"}, 400

        # Try to decrypt the hex data
        decrypted_hex = ''
        try:
            decrypted_hex = get_metrics_data(device_metrics_hex, encryption_key)
        except Exception as e:
            print(e)
            logging.error("Exception while parsing the hex data. Not able to persist.")
            return {"message": "Error parsing hex data"}, 400

        device_metrics = parse_metrics(decrypted_hex)
        logging.debug("Device Metrics Parsed: {}".format(device_metrics))

        for metrics in device_metrics.items():
            db_metric = {}
            metric = DeviceMetricType.find_by_name(metrics[0])
            logging.info(metric)

            if metric is not None:
                db_metric["metric_id"] = metric.id
            else:
                logging.error("Could not find status type for {}".format(metric["id"]))

            db_metric["metric_value"] = str(metrics[1])
            db_metric["recorded_at"] = recorded_at
            db_metric["receiver_id"] = receiver_id
            db_metric["device_serial_number"] = device_serial_number

            metric_schema = DeviceMetricSchema()
            metric = metric_schema.load(db_metric)
            metric.save_to_db()

        return {"message": "Success"}, 201



    def create_status_type(self):
        print('Device status type')
        status_type_json = request.get_json()

        status_type_schema = DeviceUiStatusTypeSchema()
        status_type = status_type_schema.load(status_type_json)

        status_type.save_to_db()

        return status_type_schema.dump(status_type), 201


    def create_metric_type(self):
        print('Device metric type')
        metric_type_json = request.get_json()
        metric_type_schema = DeviceMetricTypeSchema()
        metric_type = metric_type_schema.load(metric_type_json)

        metric_type.save_to_db()

        return metric_type_schema.dump(metric_type), 201
