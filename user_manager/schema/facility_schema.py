from schema.base_schema import BaseSchema
from model.address import Address
from marshmallow import fields, ValidationError, post_load


def must_not_blank(data):
    if not data:
        NAME_NONE = "parameter is missing"
        raise ValidationError(NAME_NONE)


class AddressSchema(BaseSchema):
    street_address_1 = fields.Str(required=True, validate=must_not_blank)
    street_address_2 = fields.Str()
    city = fields.Str(required=True, validate=must_not_blank)
    state = fields.Str(required=True, validate=must_not_blank)
    country = fields.Str(required=True, validate=must_not_blank)
    postal_code = fields.Str(required=True, validate=must_not_blank)


class AddFacilitySchema(BaseSchema):
    address = fields.Nested(AddressSchema)
    facility_name = fields.Str(required=True, validate=must_not_blank)

    @post_load
    def load_data(self, data, **kwargs):
        print(data)
        return data.get('address'), data.get('facility_name')


add_facility_schema = AddFacilitySchema()
