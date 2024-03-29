import logging

from marshmallow import ValidationError, fields, post_load
from schema.address_schema import AddressSchema
from schema.base_schema import BaseSchema
from ma import ma

def must_not_blank(data):
    if not data:
        NAME_NONE = "parameter is missing"
        raise ValidationError(NAME_NONE)


class AddFacilitySchema(BaseSchema):
    address = fields.Nested(AddressSchema, required=False)
    facility_name = fields.Str(required=True, validate=must_not_blank)
    on_call_phone = fields.Str(required=True, validate=must_not_blank)
    external_facility_id = fields.Str(required=True, validate=must_not_blank)
    primary_contact_id = fields.Int(required=False)
    all_day_phone = fields.Str(required=False)

    @post_load
    def load_data(self, data, **kwargs):
        return (
            data.get("address"),
            data.get("facility_name"),
            data.get("on_call_phone"),
            data.get("external_facility_id"),
            data.get("primary_contact_id"),
            data.get("all_day_phone")
        )


class UpdateFacilitySchema(AddFacilitySchema):
    pass


class FacilityListSchema(BaseSchema):
    page_number = fields.Int(required=True, load_only=True)
    record_per_page = fields.Int(load_only=True)
    name = fields.Str(load_only=True)
    external_id = fields.Str(load_only=True)

    @post_load
    def post_data(self, data, **kwargs):
        default_page_number = 0
        default_record_per_page = 10

        try:
            name = data.get("name", None)
            page_number = int(data.get("page_number", default_page_number))
            record_per_page = int(data.get("record_per_page", default_record_per_page))
            external_id = data.get("external_id", None)
        except ValueError as e:
            logging.error(e)
            page_number = default_page_number
            record_per_page = default_record_per_page
            name = ""
            external_id = ""
        filter_input = (page_number, record_per_page, name, external_id)
        return filter_input

class BasicFacilitySchema(ma.Schema):
    id = fields.Str(required=True)
    is_primary = fields.Boolean(required=False)

    @post_load
    def post_data(self, data, **kwargs):
        try:
            id = data.get("id", None)
            is_primary = data.get("is_primary")
        except ValueError as e:
            logging.error(e)
        return id, is_primary

class RequestBasicFacilitySchema(ma.Schema):
    facility_list = fields.List(fields.Nested(BasicFacilitySchema))

facility_list_schema = FacilityListSchema()
update_facility_schema = UpdateFacilitySchema()
add_facility_schema = AddFacilitySchema()
basic_facility_schema = BasicFacilitySchema()