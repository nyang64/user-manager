from ma import ma
from model.devices import Devices


class DeviceListSchema(ma.Schema):
    class Meta:
        model = Devices
        fields = ('serial_number', 'encryption_key', 'status')
  

device_list_schema = DeviceListSchema()
devices_list_schema = DeviceListSchema(many=True)
