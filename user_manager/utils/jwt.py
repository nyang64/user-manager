from flask import request
import jwt
from config import read_environ_value
from utils.common import tokenTime
import datetime
from werkzeug.exceptions import Unauthorized
import os
import logging
from functools import wraps
from model.user_registration import UserRegister

value = os.environ.get('SECRET_MANAGER_ARN')


def encoded_Token(
        isrefreshToken: bool,
        user_email: str,
        user_role: str = "Patient"):
    if isrefreshToken:
        secret = read_environ_value(value, "REFRESH_TOKEN_KEY")
    else:
        secret = read_environ_value(value, "ACCESS_TOKEN_KEY")
    return jwt.encode({
                "user_email": user_email,
                "user_role": user_role,
                "exp": (tokenTime(isrefreshToken)),
                "iat": datetime.datetime.now()
                }, secret)

def encoded_user_token(
        isrefreshToken: bool,
        user_email: str,
        user_role: str):
    if isrefreshToken:
        secret = read_environ_value(value, "REFRESH_TOKEN_KEY")
    else:
        secret = read_environ_value(value, "ACCESS_TOKEN_KEY")
    return jwt.encode({
                "user_email": user_email,
                "user_role": user_role,
                "exp": (tokenTime(isrefreshToken)),
                "iat": datetime.datetime.now()
                }, secret)

def require_user_token(*args):
    def require_user_token_validator(func):
        @wraps(func)
        def inner(jsonT):
            token = request.headers.get('Authorization')
            logging.info('Token is present')
            if token is None:
                logging.warning('Header value is absent')
                raise Unauthorized('Header value is absent')
            try:
                decrypted = jwt.decode(
                        token, read_environ_value(value, "ACCESS_TOKEN_KEY"),
                        algorithms=["HS256"]
                    )
            except jwt.ExpiredSignatureError:
                logging.warning('Token is Expired')
                raise Unauthorized('Token is Expired')
            except Exception:
                logging.warning('Invalid Token')
                raise Unauthorized('Invalid Token.')
            logging.info('Token Decode {}'.format(decrypted))
            user = UserRegister.find_by_email(decrypted.get('user_email', ''))
            logging.info('User found status {}'.format(user))
            if user is None:
                logging.info('User not exist')
                raise Unauthorized("User doesn't exist")
            if decrypted.get("user_role").upper() not in args:
                logging.warning('Not Permitted to this Resource')
                raise Unauthorized('Not Permitted to this Resource')
            return func(jsonT, decrypted)
        return inner
    return require_user_token_validator


def require_refresh_token(func):
    def inner(jsonT):
        token = (request.headers.get('Authorization'))
        if token is None:
            raise Unauthorized('Unauthorized Access')
        try:
            decrypt = jwt.decode(
                    token, read_environ_value(value, "REFRESH_TOKEN_KEY"),
                    algorithms=["HS256"]
                )
        except Exception:
            raise Unauthorized('Unauthorized Access')
        return func(jsonT, decrypt)
    return inner
