from model.schema.base_schema import BaseSchema
from model.devices import Devices
from marshmallow import fields, ValidationError
from utils.constants import SERIAL_NUMBER_LENGTH


def must_not_blank(data):
    print('data', type(data))
    if len(str(data)) != SERIAL_NUMBER_LENGTH:
        LESS_THEN_8 = "serial_number parameter should be a 8 digit only"
        raise ValidationError(LESS_THEN_8)


class DeviceKeySchema(BaseSchema):
    class Meta:
        model = Devices
        fields = ('serial_number', 'encryption_key')
    serial_number = fields.Int(required=True,
                               validate=must_not_blank,
                               error_messages={
                                   'required': 'parameter is missing'
                                   })


device_schema = DeviceKeySchema()
devices_schema = DeviceKeySchema(many=True)
