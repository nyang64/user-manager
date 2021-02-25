import os
import json
from werkzeug.exceptions import BadHost


def read_environ_value(value, key):
    if value is None:
        return os.environ.get(key)
    try:
        json_value = json.loads(value)
        print(json_value, type(json_value))
        return json_value.get(key, os.environ.get(key))
    except (TypeError, json.decoder.JSONDecodeError):
        print('Got Exception at Decoding')
        return os.environ.get(key)


def get_connection_url():
    print('-----------OS value-------------------')
    value = os.environ.get('user-manager-secrets')
    host = os.environ.get('POSTGRES_DB_HOST')
    port = str(os.environ.get('POSTGRES_DB_PORT'))
    database_name = os.environ.get('POSTGRES_DB_NAME')
    user = read_environ_value(value, 'POSTGRES_DB_USER_KEY')
    password = read_environ_value(value, 'POSTGRES_DB_PASSWORD_KEY')
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
