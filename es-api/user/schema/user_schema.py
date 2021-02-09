from marshmallow import fields, ValidationError
from authentication.schema.register_schema import RegisterSchema
from model.schema.base_schema import validate_number


def must_not_blank(data):
    if not data:
        NAME_NONE = "parameter is missing"
        raise ValidationError(NAME_NONE)


class CreateUserSchema(RegisterSchema):
    first_name = fields.Str(required=True,
                            validate=must_not_blank)
    last_name = fields.Str(required=True,
                           validate=must_not_blank)
    phone_number = fields.Str(required=True,
                              validate=validate_number)


create_user_schema = CreateUserSchema()