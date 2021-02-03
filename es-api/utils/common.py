import json
import datetime
import math
import random
from json import JSONEncoder
import bcrypt
from werkzeug.exceptions import BadRequest


def is_json(myjson):
    try:
        if myjson is None:
            raise BadRequest('Invalid request. Excepted JSON')
        json.dumps(myjson)
        json.loads(json.dumps(myjson))
    except Exception:
        raise BadRequest('Invalid request. Excepted JSON')
        return False
    return True


def have_keys_NotForce(myjson, *args):
    if is_json(myjson) is False:
        return False
    for arg in args:
        if arg not in myjson:
            # raise BadRequest(f'Invalid request Parameter.{arg} is missing.')
            return False
    return True


def have_keys(myjson, *args):
    if is_json(myjson) is False:
        return False
    for arg in args:
        if arg not in myjson:
            raise BadRequest(f'Invalid request Parameter.{arg} is missing.')
            return False
    return True



def tokenTime(isrefreshToken: bool):
    time_expire = 15
    now = datetime.datetime.now()
    if isrefreshToken is True:
        hours_added = datetime.timedelta(days=time_expire)
    else:
        hours_added = datetime.timedelta(minutes=time_expire)
    future_date_and_time = now + hours_added
    baseTime = datetime.datetime(
        future_date_and_time.year,
        future_date_and_time.month,
        future_date_and_time.day,
        future_date_and_time.hour,
        future_date_and_time.minute
        ).timestamp()
    return baseTime


def generateOTP():
    digits = "0123456789"
    one_time_password = ""
    for i in range(6):
        one_time_password += digits[math.floor(random.random() * 10)]
    return one_time_password


def timeDiff(first_time: datetime, second_time: datetime):
    difference = second_time - first_time
    return difference


def encPass(passW: str):
    password = bytes(passW, 'utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    return hashed.decode('utf-8')


def checkPass(passW: str, dbPassW: str):
    db_pass = bytes(dbPassW, 'utf-8')
    inp_pass = bytes(passW, 'utf-8')
    return bcrypt.checkpw(
        inp_pass,
        db_pass.decode().encode('utf-8')
        )


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class toJson(JSONEncoder):
    def default(self, o):
        return o.__dict__


class responseModel:
    def __init__(
            self,
            statusCode: str = "200",
            data: [dict] = [],
            message: str = ""):
        self.statusCode = statusCode
        self.data = data
        self.message = message

    def toJsonObj(obj):
        return json.dumps(obj, default=lambda o: o.__dict__)
