import app
import pytest
import os
from werkzeug.exceptions import BadHost


class TestApp:
    def test_app(self):
        del os.environ['POSTGRES_DB_USER_KEY']
        with pytest.raises(Exception):
            app.get_connection_url()

