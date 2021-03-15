import pytest
from config import read_environ_value


class TestClass:
    # def test_read_environ_none(self):
    #     with pytest.raises(Exception) as e:
    #         assert read_environ_value(None, None)
    #     assert "str expected, not NoneType" in str(e.value)

    def test_read_environ_blank(self):
        print(read_environ_value(
            '{\'POSTGRES_DB_PORT\':None}', 'POSTGRES_DB_PORT'))
