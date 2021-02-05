from ma import ma
from werkzeug.exceptions import BadRequest


class BaseSchema(ma.Schema):
    def handle_error(self, exc, data, **kwargs):
        raise BadRequest(str(exc))
