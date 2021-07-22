import datetime
import io
import logging
import struct
from datetime import timezone

import numpy as np
import pandas as pd
import pytz
from Crypto.Cipher import AES
from utils import constants


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
    packet.read(SYNC_BYTE).hex()

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
    length = int.from_bytes(packet.read(LENGTH), byteorder="little")

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
    associated_data = associated_data + "000000000000000000"
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
        print("Packet failed decryption with error: {}".format(e))

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
    bytes_btn_press = metrics.read(4)
    metrics_data[constants.DEVICE_BUTTON_PRESS] = int.from_bytes(
        bytes_btn_press, byteorder="little"
    )
    logging.info(f"Device Button Press {metrics_data[constants.DEVICE_BUTTON_PRESS]}")

    index += 4
    metrics.seek(index, 0)
    patchBattVolts = metrics.read(4).hex()
    logging.info("Patch Battery Volts {}".format(patchBattVolts))
    metrics_data[constants.DEVICE_PATCH_BATTERY_VOLTS] = convert_to_float(
        patchBattVolts
    )

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
    metrics_data[constants.DEVICE_ROLLING_MEAN_100] = convert_to_float(rollingMean100)

    index += 4
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

    try:
        number_ms = int.from_bytes(ts, byteorder="little")
        number_sec = number_ms / 1000
        print("Deciphered epoch: {}".format(number_sec))
        timestamp = datetime.datetime(
            2000, 1, 1, tzinfo=timezone.utc
        ) + datetime.timedelta(seconds=number_sec)
        print("Timestamp: {}".format(timestamp))
        return str(timestamp)
    except Exception as e:
        print("Error: {}".format(e))
        return ""


def convert_to_float(hex_bytes):
    little_hex = bytearray.fromhex(hex_bytes)
    little_hex.reverse()
    print("Byte array format:", little_hex)
    str_little = "".join(format(x, "02x") for x in little_hex)
    value = struct.unpack(">f", bytes.fromhex(str_little))[0]
    return value
