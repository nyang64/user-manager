from utils.validation import validate_request
from device.schema.device_key_schema import device_schema, devices_schema
from device.schema.device_status_schema import device_status_schema
from device.repository.device_repo import DeviceRepo
from utils.constants import ENCRYPTION_KEY_LENGTH
from utils.jwt import require_user_token
import uuid
import http
from utils.constants import ADMIN, ESUSER


class DeviceManager():
    def __init__(self):
        self.deviceObj = DeviceRepo()

    @require_user_token(ADMIN, ESUSER)
    def generate_key(self, decrypt):
        request_data = validate_request()
        valid = device_schema.load(request_data)
        serial_number = valid.get('serial_number')
        key = self.__generate_key(serial_number)
        device_data, msg, code = self.deviceObj.save_device_key(serial_number,
                                                                key)
        return {
            "serial_number": device_data.serial_number,
            "key": device_data.encryption_key,
            "message": msg,
            "status_code": code
        }, code

    @require_user_token(ADMIN, ESUSER)
    def devices_list(self, decrypt):
        devices = self.deviceObj.get_all_devices()
        device_json = devices_schema.dump(devices)
        return {"message": "Success",
                "data": device_json,
                "status_code": "200"}, http.client.OK

    @require_user_token(ADMIN, ESUSER)
    def add_device_type(self, decrypt):
        request_data = validate_request()
        request_data = device_status_schema.load(request_data)
        self.deviceObj.add_device_status(request_data['name'])
        return {"message": 'Success', "status": "201"}, http.client.CREATED

    def __generate_key(self, serial_number):
        """
        Generate key based on the serial number. For now, we don't have any
        requirement on the algorithm to use to generate the key. Using random to
        generate a unique key.
        :param serial_number: Device Serial Number
        :return: key: A random number
        """
        stringLength = ENCRYPTION_KEY_LENGTH
        randomString = uuid.uuid4().hex
        key = randomString.upper()[0:stringLength]
        print('key before conversion: ' + str(key))
        key = key.encode("utf-8").hex()
        print('key after conversion: ' + str(key))
        return key
