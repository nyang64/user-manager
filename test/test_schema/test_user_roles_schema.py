from unittest import TestCase

import pytest
from marshmallow import ValidationError
from model.user_roles import UserRoles
from schema.user_roles_schema import UserRolesSchema


class TestUserRoleSchema(TestCase):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    def test_user_roles_schema(self):
        args = {"role_id": 1, "user_id": 1}
        user_role = UserRolesSchema().load(args)
        self.assertIsInstance(user_role, UserRoles)

    def test_user_roles_schema_raise_exception(self):
        with pytest.raises(ValidationError) as e:
            UserRolesSchema().load("")
        print(str(e.value))
        self.assertIsInstance(e.value, ValidationError)
        self.assertIn("_schema", str(e.value))
        self.assertIn("Invalid input", str(e.value))
