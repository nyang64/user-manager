from schema.user_schema import CreateUserSchema
from marshmallow import fields, ValidationError
from ma import ma
from model.providers import Providers


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


class CreateProviderSchema(CreateUserSchema):
    facility_id = fields.Str(
        required=True,
        validate=must_not_blank)
    user_id = fields.Str(
        required=True,
        validate=must_not_blank)


class UpdateProviderSchema(CreateProviderSchema):
    provider_id = fields.Str(
        required=True,
        attribute="id",
        validate=must_not_blank)


UpdateProviderSchema = UpdateProviderSchema(many=True)
