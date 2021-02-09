from model.schema.base_schema import BaseSchema
from marshmallow import fields, validate, ValidationError


def must_not_blank(data):
    if not data:
        NAME_NONE = "parameter is missing"
        raise ValidationError(NAME_NONE)


class RegisterSchema(BaseSchema):
    email = fields.Str(required=True,
                       validate=validate.Email(error="Not a valid email"),
                       load_only=True)
    password = fields.Str(required=True,
                          validate=must_not_blank,
                          load_only=True)


register_schema = RegisterSchema()
