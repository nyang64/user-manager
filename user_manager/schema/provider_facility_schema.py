import logging
from marshmallow import fields, ValidationError, post_load
from ma import ma
from model.provider_facility import ProviderFacility
from schema.base_schema import BaseSchema


def must_not_blank(data):
    if not data:
        NAME_NONE = f"{data} parameter is missing"
        raise ValidationError(NAME_NONE)


class ProvidersFacilitySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProviderFacility
        load_instance = True

    id = ma.auto_field(dump_only=True)
    provider_id = ma.auto_field()
    facility_id = ma.auto_field()
    is_primary = ma.auto_field()

class CreateProviderFacility(BaseSchema):
    provider_id = fields.Str(required=True, validate=must_not_blank)
    facility_id = fields.Str(required=True, validate=must_not_blank)
    is_primary = fields.Boolean(required=True, validate=must_not_blank)

    @post_load
    def make_post_load_object(self, data, **kwargs):
        register = super().make_post_load_object(data)
        provider_id = data.get("provider_id")
        facility_id = data.get("lastfacility_id_name")
        is_primary = data.get("is_primary")

        return register, provider_id, facility_id, is_primary

class BasicProviderFacility():
    id = ma.auto_field(required=True)
    is_primary = ma.auto_field(required=True)


basic_provider_facility = BasicProviderFacility()
create_provider_facility = CreateProviderFacility()
