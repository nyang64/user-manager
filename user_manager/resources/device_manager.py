from flask import jsonify, request
from schema.device_metric_schema import DeviceMetricSchema
from schema.device_metric_type_schema import DeviceMetricTypeSchema
from schema.device_ui_status_schema import DeviceUiStatusSchema
from schema.device_ui_status_type_schema import DeviceUiStatusTypeSchema


class DeviceManager:
    def __init__(self):
        print('Init')

    def create_status(self):
        print('Device status')
        status_json = request.get_json()
        status_schema = DeviceUiStatusSchema()
        status = status_schema.load(status_json)

        status.save_to_db()

        return status_schema.dump(status), 201

    def create_status_type(self):
        print('Device status type')
        status_type_json = request.get_json()
        status_type_schema = DeviceUiStatusTypeSchema()
        status_type = status_type_schema.load(status_type_json)

        status_type.save_to_db()

        return status_type_schema.dump(status_type), 201

    def create_metric(self):
        print('Device metrics')
        metric_json = request.get_json()
        metric_schema = DeviceMetricSchema()
        metric = metric_schema.load(metric_json)

        metric.save_to_db()

        return metric_schema.dump(metric), 201

    def create_metric_type(self):
        print('Device metric type')
        metric_type_json = request.get_json()
        metric_type_schema = DeviceMetricTypeSchema()
        metric_type = metric_type_schema.load(metric_type_json)

        metric_type.save_to_db()

        return metric_type_schema.dump(metric_type), 201
