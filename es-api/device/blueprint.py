from flask import Blueprint
from device.device_operation.device_manager import DeviceManager


class DeviceBlueprint(Blueprint):
    def __init__(self):
        super().__init__(__class__.__name__, __name__)
        self.deviceObj = DeviceManager()
        self._add_routes()

    def _add_routes(self):
        self.add_url_rule('/device/key',
                          'Generate Key',
                          self.deviceObj.generate_key,
                          methods=['GET'])
        self.add_url_rule('/add/device/status',
                          'Add Device Status',
                          self.deviceObj.add_device_type,
                          methods=['POST'])
