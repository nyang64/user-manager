from flask import Blueprint
from device.device_operation.device_manager import DeviceManager


class DeviceBlueprint(Blueprint):
    def __init__(self):
        super().__init__(__class__.__name__, __name__)
        self.device_obj = DeviceManager()
        self._add_routes()

    def _add_routes(self):
        self.add_url_rule('/device/key',
                          'Generate Key',
                          self.device_obj.generate_key,
                          methods=['POST'])
        self.add_url_rule('/devices',
                          'List Devices',
                          self.device_obj.devices_list,
                          methods=['GET'])
        self.add_url_rule('/add/device/status',
                          'Add Device Status',
                          self.device_obj.add_device_type,
                          methods=['POST'])
