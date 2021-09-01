from marshmallow import ValidationError, fields, post_load
from schema.address_schema import AddressSchema
from schema.base_schema import BaseSchema


def must_not_blank(data):
    if not data:
        NAME_NONE = "parameter is missing"
        raise ValidationError(NAME_NONE)


class AddFacilitySchema(BaseSchema):
    address = fields.Nested(AddressSchema, required=False)
    facility_name = fields.Str(required=True, validate=must_not_blank)
    on_call_phone = fields.Str(required=True, validate=must_not_blank)
    external_facility_id = fields.Str(required=True, validate=must_not_blank)

    @post_load
    def load_data(self, data, **kwargs):
        return data.get("address"), data.get("facility_name"), data.get("on_call_phone"), data.get("external_facility_id")


class UpdateFacilitySchema(AddFacilitySchema):
    pass


update_facility_schema = UpdateFacilitySchema()
add_facility_schema = AddFacilitySchema()
