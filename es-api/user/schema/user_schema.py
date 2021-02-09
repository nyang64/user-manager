from marshmallow import fields, ValidationError, post_load
from authentication.schema.register_schema import RegisterSchema
from model.schema.base_schema import validate_number, BaseSchema


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
    
    @post_load
    def post_load_object(self, data, **kwargs):
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        phone_number = data.get('phone_number')
        register = (email, password)
        user = (first_name, last_name, phone_number)
        return register, user
    

create_user_schema = CreateUserSchema()


class UpdateUserSchema(BaseSchema):
    first_name = fields.Str(required=True,
                            validate=must_not_blank)
    last_name = fields.Str(required=True,
                           validate=must_not_blank)
    phone_number = fields.Str(required=True,
                              validate=validate_number)
    
    @post_load
    def post_load_object(self, data, **kwargs):
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        phone_number = data.get('phone_number')
        return first_name, last_name, phone_number


update_user_schema = UpdateUserSchema()
