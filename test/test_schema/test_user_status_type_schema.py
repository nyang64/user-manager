from unittest import TestCase

from schema.user_status_type_schema import UserStatusTypeSchema
from model.user_status_type import UserStatusType

class TestUserStatusTypeSchema(TestCase):

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    def test_user_status_type_schema(self):
        args = {"name": "test"}
        type = UserStatusTypeSchema().load(args)
        self.assertIsInstance(type, UserStatusType)