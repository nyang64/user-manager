from user.schema.user_schema import CreateUserSchema
from marshmallow import fields, ValidationError


def must_not_blank(data):
    if not data:
        NAME_NONE = f"{data} parameter is missing"
        raise ValidationError(NAME_NONE)


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
