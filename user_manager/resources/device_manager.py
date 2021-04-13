from flask import jsonify, request
from schema.device_metric_schema import DeviceMetricSchema
from schema.device_metric_type_schema import DeviceMetricTypeSchema
from schema.device_ui_status_schema import DeviceUiStatusSchema
from schema.device_ui_status_type_schema import DeviceUiStatusTypeSchema
from utils.validation import validate_request

from model.device_metric_type import DeviceMetricType
import logging

class DeviceManager:
    def __init__(self):
        logging.info("In Device Manager")

    def create_status(self):
        logging.info('Persisting UI status messages')
        status_json = validate_request()
        logging.info(status_json)

        statuses = status_json.get('statuses')

        for status in statuses:
            ui_status = {}
            ui_status['device_serial_number'] = status_json.get('device_serial_number')
            ui_status['receiver_recorded_at'] = status_json.get('received_at')
            ui_status['receiver_id'] = status_json.get('receiver_id')
            ui_status['recorded_at'] = status.get('recorded_at')
            ui_status['ui_status_id'] = status.get('ui_id')
            schema = DeviceUiStatusSchema()
            model = schema.load(ui_status)
            model.save_to_db()

        return {"message": "Device Status"}, 201


    def create_metric(self):
        logging.info('Persisting UI status messages')
        metric_json = request.get_json()

        logging.info(metric_json)
        metric = DeviceMetricType.find_by_name(metric_json["name"])
        del metric_json["name"]
        metric_json["metric_id"] = metric.id

        metric_schema = DeviceMetricSchema()
        metric = metric_schema.load(metric_json)

        metric.save_to_db()

        return {"message": "Success"}, 201

    def create_metric_type(self):
        print('Device metric type')
        metric_type_json = request.get_json()
        metric_type_schema = DeviceMetricTypeSchema()
        metric_type = metric_type_schema.load(metric_type_json)

        metric_type.save_to_db()

        return metric_type_schema.dump(metric_type), 201

    def create_status_type(self):
        print('Device status type')
        status_type_json = request.get_json()

        status_type_schema = DeviceUiStatusTypeSchema()
        status_type = status_type_schema.load(status_type_json)

        status_type.save_to_db()

        return status_type_schema.dump(status_type), 201
