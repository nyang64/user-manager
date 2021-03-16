import os
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.ERROR)


def read_environ_value(value, key):
    if value is None:
        return os.environ.get(key)
    try:
        json_value = json.loads(value)
        return json_value.get(key, os.environ.get(key))
    except (TypeError, json.decoder.JSONDecodeError):
        logger.error('Got Exception at Decoding')
        print('Got Exception at Decoding')
        return os.environ.get(key)


def get_connection_url():
    return os.environ.get("SQLALCHEMY_DATABASE_URI")
