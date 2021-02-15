from marshmallow import (
    fields, ValidationError)
from werkzeug.exceptions import BadRequest
from marshmallow_sqlalchemy import ModelSchema
from sqlalchemy.orm import sessionmaker, scoped_session
from db import db


class UserUpdateSchema(ModelSchema):

    def must_not_blank(data):
        if not data:
            NOT_NONE = "cannot be null"
            raise ValidationError(NOT_NONE)

    user_email = fields.Str(
        required=True,
        validate=must_not_blank)
    newpassword = fields.Str(
        required=True,
        validate=must_not_blank)

    @classmethod
    def validate_data(cls, data):
        try:
            session = scoped_session(sessionmaker(bind=db))
            data_obj = user_update_schema.validate(data=data, session=session)
            if(data_obj):
                raise BadRequest(data_obj)
            else:
                return data
        except Exception as e:
            raise BadRequest(e)


user_update_schema = UserUpdateSchema()
