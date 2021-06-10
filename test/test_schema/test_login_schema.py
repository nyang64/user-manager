from unittest import TestCase

import pytest
from marshmallow import ValidationError
from schema.login_schema import UserLoginSchema
from werkzeug.exceptions import BadRequest


class TestLoginSchema(TestCase):
    def test_validate_data(self):
        with pytest.raises(BadRequest) as e:
            UserLoginSchema.validate_data(None)
        self.assertIsInstance(e.value, BadRequest)
