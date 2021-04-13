from flask import Blueprint
from resources.device_manager import DeviceManager


class DeviceBlueprint(Blueprint):
    def __init__(self):
        super().__init__(__class__.__name__, __name__)
        self.device_mgr = DeviceManager()
        self._add_routes()

    def _add_routes(self):
        self.add_url_rule('/devices/statuses', 'Create device status',
                          self.device_mgr.create_status,
                          methods=['POST'])
        self.add_url_rule('/devices/status_types', 'Create device status type',
                          self.device_mgr.create_status_type,
                          methods=['POST'])
        self.add_url_rule('/devices/metrics', 'Create device metric',
                          self.device_mgr.create_metric,
                          methods=['POST'])
        self.add_url_rule('/devices/metric_types', 'Create device metric type',
                          self.device_mgr.create_metric_type,
                          methods=['POST'])
