from flask import Blueprint
from resources.device_manager import DeviceManager


class DeviceBlueprint(Blueprint):
    def __init__(self):
        super().__init__(__class__.__name__, __name__)
        self.device_mgr = DeviceManager()
        self._add_routes()

    def _add_routes(self):
        self.add_url_rule('/device/status', 'Create device status',
                          self.device_mgr.create_status,
                          methods=['POST'])
        self.add_url_rule('/device/status_types', 'Create device status type',
                          self.device_mgr.create_status_type,
                          methods=['POST'])
        self.add_url_rule('/device/metrics', 'Create device metric',
                          self.device_mgr.create_metric,
                          methods=['POST'])
        self.add_url_rule('/device/metrics_types', 'Create device metric type',
                          self.device_mgr.create_metric_type,
                          methods=['POST'])
