from ma import ma
from marshmallow import ValidationError, fields, post_load
from model.users import Users
from schema.base_schema import BaseSchema, validate_number
from schema.register_schema import RegisterSchema, RegistrationSchema
from schema.role_schema import RoleSchema


def must_not_blank(data):
    if not data:
        NAME_NONE = "parameter is missing"
        raise ValidationError(NAME_NONE)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        load_instance = True

    id = ma.auto_field(dump_only=True)
    registration_id = ma.auto_field()
    registration = ma.Nested(RegistrationSchema())
    role = ma.Nested(RoleSchema())


class CreateUserSchema(RegisterSchema):
    first_name = fields.Str(required=True, validate=must_not_blank)
    last_name = fields.Str(required=True, validate=must_not_blank)
    phone_number = fields.Str(required=True, validate=validate_number)
    role_name = fields.Str(required=True, validate=must_not_blank)
    external_user_id = fields.Str(reqired=True)

    @post_load
    def make_post_load_object(self, data, **kwargs):
        register = super().make_post_load_object(data)
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        phone_number = data.get("phone_number")
        role_name = data.get("role_name")
        external_user_id = data.get("external_user_id")
        user = (first_name, last_name, phone_number, role_name, external_user_id)
        return register, user


create_user_schema = CreateUserSchema()


class UpdateUserSchema(BaseSchema):
    first_name = fields.Str(required=True, validate=must_not_blank)
    last_name = fields.Str(required=True, validate=must_not_blank)
    phone_number = fields.Str(required=True, validate=validate_number)

    @post_load
    def post_load_object(self, data, **kwargs):
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        phone_number = data.get("phone_number")
        return first_name, last_name, phone_number


update_user_schema = UpdateUserSchema()
