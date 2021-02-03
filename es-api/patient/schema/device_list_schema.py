from marshmallow_sqlalchemy import ModelSchema
from model.devices import Devices


class DeviceListSchema(ModelSchema):
    class Meta:
        model = Devices
        fields = ('serial_number', 'encryption_key', 'status')
