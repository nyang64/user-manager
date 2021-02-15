from ma import ma
from werkzeug.exceptions import BadRequest
from marshmallow import ValidationError


def validate_number(data):
    if data is None:
        raise ValidationError('phone_number cannot be None')
    elif not data.isdecimal():
        raise ValidationError('phone_number should be numeric')
    elif len(data) != 10:
        raise ValidationError('Number less than 10 digit')


class BaseSchema(ma.Schema):
    def handle_error(self, exc, data, **kwargs):
        raise BadRequest(str(exc))
