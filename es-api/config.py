import os
from werkzeug.exceptions import BadHost


def get_connection_url():
    host = os.environ.get('POSTGRES_DB_HOST')
    port = str(os.environ.get('POSTGRES_DB_PORT'))
    database_name = os.environ.get('POSTGRES_DB_NAME')
    user = os.environ.get('POSTGRES_DB_USER_KEY')
    password = os.environ.get('POSTGRES_DB_PASSWORD_KEY')
    if (
        host is None or
        port is None or
        database_name is None or
        user is None or
        password is None
    ):
        raise BadHost('Database connection error')
    return f"postgresql://{user}:{password}@{host}:{port}/{database_name}"
