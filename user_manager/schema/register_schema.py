from schema.base_schema import BaseSchema
from marshmallow import fields, validate, ValidationError, post_load
from model.user_registration import UserRegister
from ma import ma


def must_not_blank(data):
    if not data:
        NAME_NONE = "parameter is missing"
        raise ValidationError(NAME_NONE)


class RegistrationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserRegister
        load_instance = True

    id = ma.auto_field(dump_only=True)
    password = ma.auto_field(load_only=True)


class RegisterSchema(BaseSchema):
    email = fields.Str(required=True,
                       validate=validate.Email(error="Not a valid email"),
                       load_only=True)
    password = fields.Str(required=False,
                          validate=must_not_blank,
                          load_only=True)

    @post_load
    def make_post_load_object(self, data, **kwargs):
        email = str(data.get('email')).lower()
        password = data.get('password')
        register = (email, password)
        return register


register_schema = RegisterSchema()
