from config import read_environ_value


class TestCommon:
    def test_read_environ_blank(self):
        print(read_environ_value(
            '{\'POSTGRES_DB_PORT\':None}', 'POSTGRES_DB_PORT'))
