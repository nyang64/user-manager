from flask import request
import jwt
import os
from utils.common import tokenTime
import datetime
from werkzeug.exceptions import Unauthorized


def encoded_Token(
        isrefreshToken: bool,
        user_email: str,
        user_role: str = "Patient"):
    if isrefreshToken:
        secret = os.environ["REFRESH_TOKEN_KEY"]
    else:
        secret = os.environ["ACCESS_TOKEN_KEY"]
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
                return {"Message": "Unauthorized Access"}, 401
            try:
                decrypted = jwt.decode(
                        token, os.environ["ACCESS_TOKEN_KEY"],
                        algorithms=["HS256"]
                    )
            except jwt.ExpiredSignatureError:
                raise Unauthorized(f'Token is Expired')

            except Exception as e:
                raise Unauthorized(f'Invalid Token')
            print(decrypted["user_role"].upper(), args)
            if decrypted["user_role"].upper() not in args:
                raise Unauthorized(f'Not Permitted to this Resource')
            return func(jsonT, decrypted)
        return inner
    return require_user_token_validator


def require_refresh_token(func):
    def inner(jsonT):
        token = (request.headers.get('Authorization'))
        if token is None:
            return {"Message": "Unauthorized Access"}, 401
        try:
            decrypt = jwt.decode(
                    token, os.environ["REFRESH_TOKEN_KEY"],
                    algorithms=["HS256"]
                )
        except Exception:
            return {"Message": "Unauthorized Access"}, 401
        print(decrypt)
        return func(jsonT, decrypt)
    return inner
