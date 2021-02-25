import os
import json
from werkzeug.exceptions import BadHost


def read_environ_value(key):
    value = os.environ.get(key)
    try:
        if len(value.split(':')) == 2:
            print('Convert to JSON')
            json_value = json.loads(value)
            print(json_value, type(json_value))
            return json_value.get(key, os.environ.get(key))
        else:
            print('Not a JSON')
            return value
    except (TypeError, json.decoder.JSONDecodeError):
        print('Got Exception at Decoding')
        return os.environ.get(key)


def get_connection_url():
    print('-----------OS value-------------------')
    host = read_environ_value('POSTGRES_DB_HOST')
    port = str(read_environ_value('POSTGRES_DB_PORT'))
    database_name = read_environ_value('POSTGRES_DB_NAME')
    user = read_environ_value('POSTGRES_DB_USER_KEY')
    password = read_environ_value('POSTGRES_DB_PASSWORD_KEY')
    print('db------', host, port, database_name, user, password)
    if (
        host is None or
        port is None or
        database_name is None or
        user is None or
        password is None
    ):
        raise BadHost('Database connection error')
    return f"postgresql://{user}:{password}@{host}:{port}/{database_name}"
