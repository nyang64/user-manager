import json
import logging
import os

import requests
from config import read_environ_value
from utils.constants import ASSIGNED, AVAILABLE, DEVICE_INFO_MOCK, FAKE_TOKEN, FLASK_ENV
from werkzeug.exceptions import InternalServerError, NotFound


class DeviceManagerApi:
    value = os.environ.get("SECRET_MANAGER_ARN")
    base_url = read_environ_value(value, "DEVICE_BASE_URL")

    @classmethod
    def check_device_exists(cls, device_serial_number):
        if FLASK_ENV == "local":
            return True

        header = {"Authorization": cls.get_auth_token()}
        payload = {"serial_number": device_serial_number}
        url = cls.base_url + "/device/exists"
        device_exists = False

        response = requests.get(url, headers=header, params=payload)

        if response.status_code == 200:
            device_exists = True

        return device_exists

    @classmethod
    def update_device_status(cls, device_serial_number, status):
        if FLASK_ENV == "local":
            return True

        header = {"Authorization": cls.get_auth_token()}
        payload = {"serial_number": device_serial_number, "name": status}
        url = cls.base_url + "/update/device/status"
        updated = None

        response = requests.post(url, headers=header, json=payload)

        if response.status_code == 201:
            updated = True

        logging.info(f"API response {response.text}")

        return updated

    @classmethod
    def get_device(cls, device_serial_number):
        if FLASK_ENV == "local":
            return DEVICE_INFO_MOCK

        header = {"Authorization": cls.get_auth_token()}
        payload = {"serial_number": str(device_serial_number)}
        url = cls.base_url + "/device"
        device_info = {}

        response = requests.get(url, headers=header, params=payload)

        if response.status_code == 200:

            response_body = json.loads(response.text)
            device_info = {
                "key": response_body["data"]["encryption_key"],
                "serial_number": response_body["data"]["serial_number"],
            }

        logging.info(f"API 'get_device' response: {response.text}")

        return device_info

    @classmethod
    def get_device_status(cls, device_serial_number):
        if FLASK_ENV == "local":
            return AVAILABLE

        header = {"Authorization": cls.auth_token()}
        payload = {"serial_number": device_serial_number}
        url = cls.base_url + "/get/device/status"
        device_status = None

        response = requests.get(url, headers=header, params=payload)

        if response.status_code == 200:
            device_status = json.loads(response.text)["data"]

        logging.info(f"API: 'get_device_status' response: {device_status}")

        return device_status

    @classmethod
    def get_auth_token(cls):
        if FLASK_ENV == "local":
            return FAKE_TOKEN

        url = cls.base_url + "/login"
        id_token = None

        request_body = {
            "email": read_environ_value(cls.value, "DEVICE_EMAIL"),
            "password": read_environ_value(cls.value, "DEVICE_PASSWORD"),
        }

        response = requests.post(url, json=request_body)

        if response.status_code == 200:
            response_body = json.loads(response.text)
            id_token = response_body["id_token"]

        logging.info(
            f"API: 'get_auth_token' response status_code: {response.status_code}"
        )

        if not id_token:
            raise InternalServerError("Could not log in to device manager")

        return id_token
