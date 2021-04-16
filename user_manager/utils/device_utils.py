from config import read_environ_value
from utils import constants
import json
import os
import io
import requests
import logging
from Crypto.Cipher import AES
import struct
import datetime
from datetime import timezone
import numpy as np
import pandas as pd
import pytz


def get_encryption_key(serial_number):
    token = get_device_services_auth_token()
    header = {'Authorization': token}
    payload = {'serial_number': serial_number}
    logging.info('API calling {}'.format(constants.GET_DEVICE_DETAIL_URL))
    logging.info('payload {}'.format(payload))
    try:
        response = requests.get(constants.GET_DEVICE_DETAIL_URL,
                         headers=header,
                         params=payload)
    except Exception as e:
        logging.error(e)
        response = None

    logging.info('Request finished {}'.format(response.status_code))
    logging.info('Response {}'.format(response.text))

    if response is not None and response.status_code == 200:
        response = json.loads(response.text)
        logging.info('API response {}'.format(response))
        return response['data']['encryption_key']
    else:
        return None


def get_device_services_auth_token():
    value = os.environ.get('SECRET_MANAGER_ARN')
    device_email = read_environ_value(value, 'DEVICE_EMAIL')
    device_password = read_environ_value(value, 'DEVICE_PASSWORD')
    data = {"email": device_email, "password": device_password}
    resp = requests.post(constants.LOGIN_URL, json=data)
    if resp.status_code == 200:
        return json.loads(resp.text).get('id_token')
    else:
        return None


def get_metrics_data(packet_hex, key_hex):
    SYNC_BYTE = 1
    INIT_VECTOR = 12
    VERSION = 2
    TYPE = 1
    SUB_TYPE = 1
    SEQUENCE = 1
    LENGTH = 2
    TAG = 16

    key = bytes.fromhex(key_hex)
    bytes_hex = bytes.fromhex(packet_hex)
    packet = io.BytesIO(bytes_hex)

    # Seek a specific position in the file and read N bytes
    # start with the sync byte - should start with AA
    index = 0
    packet.seek(index, 0)
    sync = packet.read(SYNC_BYTE).hex()

    index += 1
    packet.seek(index, 0)
    vector = packet.read(INIT_VECTOR).hex()

    index += INIT_VECTOR
    packet.seek(index, 0)
    version = packet.read(VERSION).hex()

    index += VERSION
    packet.seek(index, 0)
    type = packet.read(TYPE).hex()

    index += TYPE
    packet.seek(index, 0)
    sub_type = packet.read(SUB_TYPE).hex()

    index += SUB_TYPE
    packet.seek(index, 0)
    sequence = packet.read(SEQUENCE).hex()

    index += SEQUENCE
    packet.seek(index, 0)
    length_hex = packet.read(LENGTH).hex()

    packet.seek(index, 0)
    length = int.from_bytes(packet.read(LENGTH), byteorder='little')

    index += LENGTH
    packet.seek(index, 0)
    data = packet.read(length).hex()

    index += int(length)
    packet.seek(index, 0)
    tag = packet.read(TAG).hex()

    # Verify the data integrity of the packet
    ####################################################################################
    nonce = bytes.fromhex(vector)
    tag = bytes.fromhex(tag)
    ciphertext = bytes.fromhex(data)

    associated_data = version + type + sub_type + sequence + length_hex
    associated_data = associated_data + '000000000000000000'
    associated_data_bytes = bytes.fromhex(associated_data)

    cipher = AES.new(key, AES.MODE_GCM, nonce)
    cipher.update(associated_data_bytes)

    # decrypt the data
    plaintext = cipher.decrypt(ciphertext)
    print(f"decrypted data: {plaintext.hex()}")
    metrics_data = None
    try:
        cipher.verify(tag)
        print("\n")
        metrics_data = plaintext.hex()
        print("\n")
    except Exception as e:
        print(e)
        output_message = "Packet failed decryption with error: {}".format(e)

    return metrics_data


def parse_metrics(metrics_hex):

    """
    Parse the device metrics data. Device metrics has a fixed structure which can change
    later. Current structure from firmware is
        {
           uint32_t buttonPresses;  #4 bytes
           float32_t patchBattVolts; #4 bytes
           float32_t auxBattVolts; #4 bytes
           float32_t rollingMean32; #4 bytes
           float32_t rollingMean100; #4 bytes
           uint64_t timestamp; #8 bytes
           uint8_t padding[4] ; // Padding to make the message multiple of 16 bytes
        }
    """
    metrics_data = {}
    bytes_hex = bytes.fromhex(metrics_hex)
    metrics = io.BytesIO(bytes_hex)

    logging.info("Raw device metrics {}".format(bytes_hex))

    index = 0
    metrics.seek(index, 0)
    buttonPresses = metrics.read(4).hex()
    logging.info("Device Button Press {}".format(buttonPresses))
    metrics_data[constants.DEVICE_BUTTON_PRESS] = int(buttonPresses, 8)

    index += 4
    metrics.seek(index, 0)
    patchBattVolts = metrics.read(4).hex()
    logging.info("Patch Battery Volts {}".format(patchBattVolts))
    metrics_data[constants.DEVICE_PATCH_BATTERY_VOLTS] = convert_to_float(patchBattVolts)

    index += 4
    metrics.seek(index, 0)
    auxBattVolts = metrics.read(4).hex()
    logging.info("Aux Battery Volts {}".format(auxBattVolts))
    metrics_data[constants.DEVICE_AUX_BATTERY_VOLTS] = convert_to_float(auxBattVolts)

    index += 4
    metrics.seek(index, 0)
    rollingMean32 = metrics.read(4).hex()
    logging.info("Rolling Mean 32 {}".format(rollingMean32))
    metrics_data[constants.DEVICE_ROLLING_MEAN_32] = convert_to_float(rollingMean32)

    index += 4
    metrics.seek(index, 0)
    rollingMean100 = metrics.read(4).hex()
    logging.info("Rolling Mean 100 {}".format(rollingMean100))
    metrics_data[constants.DEVICE_ROLLING_MEAN_100] = convert_to_float(rollingMean32)

    index += 8
    metrics.seek(index, 0)
    timestamp = metrics.read(8).hex()
    logging.info("Timestamp {}".format(timestamp))
    metrics_data[constants.DEVICE_METRICS_TIMESTAMP] = decipher_ts(timestamp)

    logging.info(metrics_data)
    return metrics_data


def decipher_ts(timestamp):
    new_ts = bytearray.fromhex(timestamp)
    ts = np.frombuffer(new_ts, dtype=np.uint8)

    bytes_per_ts = 1
    ts = ts.reshape(-1, bytes_per_ts)
    TS_COL = ['ts_y_m_d', 'ts_hr_min_sec_ms', 'ts', 'samples']
    df = pd.DataFrame(columns=TS_COL, index=range(len(ts)))
    df.index.name = 'seg_num'


    try:
        number_ms = int.from_bytes(ts, byteorder='little')
        number_sec = number_ms/1000
        print("Deciphered epoch: {}".format(number_sec))
        timestamp = datetime.datetime.utcfromtimestamp(number_sec)
        tz = pytz.timezone('America/Los_Angeles')
        print(tz)
        timestamp = datetime.datetime(2000, 1, 1, tzinfo=timezone.utc) + datetime.timedelta(seconds=number_sec)
        print("Timestamp: {}".format(timestamp))
        return str(timestamp)
    except Exception as e:
        print("Error: {}".format(e))
        return ""


def convert_to_float(hex_bytes):
    little_hex = bytearray.fromhex(hex_bytes)
    little_hex.reverse()
    print("Byte array format:", little_hex)
    str_little = ''.join(format(x, '02x') for x in little_hex)
    value = struct.unpack('>f', bytes.fromhex(str_little))[0]
    return value