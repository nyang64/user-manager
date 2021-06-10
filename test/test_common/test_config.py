from unittest import TestCase

from config import get_connection_url, read_environ_value


class TestConfig(TestCase):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    def test_read_environ_value(self):
        resp = read_environ_value(None, "Key")
        self.assertIsNone(resp)
