from model.schema.base_schema import BaseSchema
from model.device_status_types import DeviceStatusType
from marshmallow import fields, ValidationError


def must_not_blank(data):
    if not data:
        NOT_NONE = "name cannot be null"
        raise ValidationError(NOT_NONE)


class DeviceStatusSchema(BaseSchema):
    class Meta:
        model = DeviceStatusType
        fields = ('name', 'created_at')
    name = fields.Str(required=True,
                      validate=must_not_blank,
                      error_messages={
                          'required': 'parameter is missing'
                          })


device_status_schema = DeviceStatusSchema()
devices_status_schema = DeviceStatusSchema(many=True)
