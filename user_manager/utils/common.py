import json
import datetime
import math
import random
from json import JSONEncoder
import bcrypt
from werkzeug.exceptions import BadRequest
import uuid


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


def generate_uuid():
    return str(uuid.uuid4())


def timeDiff(first_time: datetime, second_time: datetime):
    difference = second_time - first_time
    return difference


def encPass(passW: str):
    password = bytes(passW, 'utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    return hashed.decode('utf-8')


def checkPass(passW: str, dbPassW: str):
    return bcrypt.checkpw(
        passW.encode('utf-8'),
        dbPassW.encode('utf-8')
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
            status_code: str = "200",
            data: [dict] = [],
            message: str = ""):
        self.status_code = status_code
        self.data = data
        self.message = message

    def toJsonObj(obj):
        return json.dumps(obj, default=lambda o: o.__dict__)


class auth_response_model:
    def __init__(
            self,
            message: str, first_name: str,
            id_token: str, last_name: str,
            refresh_token: str = "", user_status: str = 'Provider',
            isFirstTimeLogin: bool = False,):
        self.message = message
        self.id_token = id_token
        self.refresh_token = refresh_token
        self.isFirstTimeLogin = isFirstTimeLogin
        self.user_status = user_status.capitalize()
        self.first_name = first_name.capitalize()
        self.last_name = last_name.capitalize()

    def toJsonObj(obj):
        return json.loads(json.dumps(obj, default=lambda o: o.__dict__))


def generate_signed_url(report_key=None):
    '''
    Verify the key and Generate the signed report url
    :param: report_key
    :return: report_signed_url
    '''
    from utils.constants import REPORT_BUCKET_NAME
    import boto3
    from botocore.exceptions import ClientError
    try:
        s3_client = boto3.client('s3')
        resp = s3_client.list_objects_v2(Bucket=REPORT_BUCKET_NAME,
                                         Prefix=report_key)
        key_exists = True if 'Contents' in resp else False
        if key_exists:
            presign_url = s3_client.generate_presigned_url(
                    'get_object', Params={
                        'Bucket': REPORT_BUCKET_NAME, 'Key': report_key},
                    ExpiresIn=600)
            return presign_url
        else:
            return "Report doesn't exists"
    except ClientError:
        return "Error while generation URL"


def rename_keys(original, transform):
    return dict([(transform.get(k), v) for k, v in original.items()])
