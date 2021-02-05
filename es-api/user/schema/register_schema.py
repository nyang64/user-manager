from marshmallow import fields, validate
from model.schema.base_schema import BaseSchema


class RegisterSchema(BaseSchema):
    email = fields.Str(required=True,
                       validate=validate.Email(error="Not a valid email"))
    password = fields.Str(required=True,
                          validate=validate.Length(min=1, error='password \
                                                   cannot be None'))


register_schema = RegisterSchema()
