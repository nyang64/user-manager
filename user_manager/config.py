import json
import logging
import os

from werkzeug.exceptions import BadHost

arn_value = os.environ.get("SECRET_MANAGER_ARN")


def read_environ_value(value, key):
    if value is None:
        return os.environ.get(key)
    try:
        json_value = json.loads(value)
        return json_value.get(key, os.environ.get(key))
    except (TypeError, json.decoder.JSONDecodeError):
        logging.error("Got Exception at Decoding")
        print("Got Exception at Decoding")
        return os.environ.get(key)


def get_connection_url():
    host = read_environ_value(arn_value, "POSTGRES_DB_HOST")
    port = read_environ_value(arn_value, "POSTGRES_DB_PORT")
    database_name = read_environ_value(arn_value, "POSTGRES_DB_NAME")
    user = read_environ_value(arn_value, "POSTGRES_DB_USER_KEY")
    password = read_environ_value(arn_value, "POSTGRES_DB_PASSWORD_KEY")
    print(f"postgresql://{user}:{password}@{host}:{port}/{database_name}")
    if (
        host is None
        or port is None
        or database_name is None
        or user is None
        or password is None
    ):
        raise BadHost("Database connection error")
    return f"postgresql://{user}:{password}@{host}:{port}/{database_name}"
