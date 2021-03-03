from flask import request
import jwt
from config import read_environ_value
from utils.common import tokenTime
import datetime
from werkzeug.exceptions import Unauthorized
import os

value = os.environ.get('user-manager-secrets')


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


def require_user_token(*args):
    def require_user_token_validator(func):
        def inner(jsonT):
            token = (request.headers.get('Authorization'))
            if token is None:
                raise Unauthorized('Token is Expired')
            try:
                decrypted = jwt.decode(
                        token, read_environ_value(value, "ACCESS_TOKEN_KEY"),
                        algorithms=["HS256"]
                    )
            except jwt.ExpiredSignatureError:
                raise Unauthorized('Token is Expired')

            except Exception:
                raise Unauthorized('Invalid Token.')
            if decrypted["user_role"].upper() not in args:
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
