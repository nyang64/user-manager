import logging

from schema.user_schema import CreateUserSchema
from marshmallow import fields, ValidationError, post_load
from ma import ma
from model.providers import Providers
from model.users import Users
from schema.base_schema import BaseSchema


def must_not_blank(data):
    if not data:
        NAME_NONE = f"{data} parameter is missing"
        raise ValidationError(NAME_NONE)


class ProvidersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Providers
        load_instance = True

    id = ma.auto_field(dump_only=True)
    user_id = ma.auto_field()
    facility_id = ma.auto_field()
    is_primary = ma.auto_field()


class CreateProviderSchema(CreateUserSchema):
    facility_id = fields.Str(
        required=True,
        validate=must_not_blank)
    user_id = fields.Str(
        required=True,
        validate=must_not_blank)


class UpdateProviderSchema(BaseSchema):
    first_name = fields.Str(required=False)
    last_name = fields.Str(required=False)
    external_user_id = fields.Str(required=False)
    phone_number = fields.Str(required=False)
    email = fields.Str(required=False)
    facility_id = fields.Int(required=False)

    @post_load
    def load_data(self, data, **kwargs):
        facility_id = data.get("facility_id")
        user = Users(first_name=data.get("first_name"),
                     last_name=data.get("last_name"),
                     phone_number=data.get("phone_number"),
                     external_user_id=data.get("external_user_id"))
        email = data.get("email")
        return facility_id, email, user


UpdateProviderSchema = UpdateProviderSchema()


class ProviderListSchema(BaseSchema):
    page_number = fields.Int(required=True, load_only=True)
    record_per_page = fields.Int(load_only=True)
    name = fields.Str(load_only=True)

    @post_load
    def post_data(self, data, **kwargs):
        try:
            name = data.get("name", None)
            page_number = int(data.get("page_number", 0))
            record_per_page = int(data.get("record_per_page", 10))
        except ValueError as e:
            logging.error(e)
            page_number = 0
            record_per_page = 10
            name = ""
        filter_input = (
            page_number,
            record_per_page,
            name
        )
        return filter_input


provider_list_schema = ProviderListSchema()
