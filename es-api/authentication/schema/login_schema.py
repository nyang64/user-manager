from model.user_registration import UserRegister
from marshmallow import (
    fields, ValidationError, validate)
from werkzeug.exceptions import BadRequest
from marshmallow_sqlalchemy import ModelSchema
from sqlalchemy.orm import sessionmaker, scoped_session
from db import db


class UserLoginSchema(ModelSchema):

    def must_not_blank(data):
        if not data:
            NOT_NONE = "cannot be null"
            raise ValidationError(NOT_NONE)

    email = fields.Str(
        required=True,
        validate=validate.Email(
            error="Not a valid email address"), error_messages={
                'required': 'Email is mandatory field.'
                }
            )
    password = fields.Str(
        required=True,
        validate=must_not_blank)

    class Meta:
        model = UserRegister
        dump_only = ("id",)
        include_fk = True

    @classmethod
    def validate_data(cls, data) -> "UserRegister":
        try:
            session = scoped_session(sessionmaker(bind=db))
            data_obj = user_login_schema.validate(data=data, session=session)
            if(data_obj):
                raise BadRequest(data_obj)
            else:
                return user_login_schema.load(data)
        except Exception as e:
            raise BadRequest(e)


user_login_schema = UserLoginSchema()
