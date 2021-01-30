import json
import datetime
import math
import random
from json import JSONEncoder
import bcrypt


def is_json(myjson):
    try:
        if myjson is None:
            return False
        json.dumps(myjson)
        json.loads(json.dumps(myjson))
    except Exception:
        return False
    return True


def have_keys(myjson, *args):
    if is_json(myjson) is False:
        return False
    for arg in args:
        if arg not in myjson:
            return False
    return True


def tokenTime(isrefreshToken: bool):
    timeT = 15
    now = datetime.datetime.now()
    if isrefreshToken is True:
        hours_added = datetime.timedelta(days=timeT)
    else:
        hours_added = datetime.timedelta(minutes=timeT)
    # print("c", hours_added)
    future_date_and_time = now + hours_added
    # print("e", future_date_and_time)
    baseTime = datetime.datetime(
        future_date_and_time.year,
        future_date_and_time.month,
        future_date_and_time.day,
        future_date_and_time.hour,
        future_date_and_time.minute
        ).timestamp()
    # print('datedelta',str(hours_added))
    # print("b", baseTime)
    return baseTime

    # def tokenTime():
    # hours = 2
    # now = datetime.datetime.now()
    # hours_added = datetime.datetime(now.year,now.month,now.day, now.hour+
    # hours,now.minute).timestamp()
    # # print('datedelta',str(hours_added))
    # return hours_added


def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


def timeDiff(first_time: datetime, second_time: datetime):
    difference = second_time - first_time
    print(difference)


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
