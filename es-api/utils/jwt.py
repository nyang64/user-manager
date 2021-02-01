from flask import request
import jwt
import os
from utils.common import tokenTime
import datetime


def encoded_Token(
        isrefreshToken: bool,
        user_email: str,
        user_role: str = "Patient"):
    if isrefreshToken:
        secret = os.environ["refresh_token_key"]
    else:
        secret = os.environ["access_token_key"]
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
                        token, os.environ["access_token_key"],
                        algorithms=["HS256"]
                    )
            except jwt.ExpiredSignatureError:
                return {"Message": "Token is Expired"}

            except Exception as e:
                return {"Message": "Unauthorized Access"}, 401

            if decrypted["user_role"] not in args:
                return {"Message": "Unauthorized For This Resource"}, 401

            return func(jsonT, decrypted)
        return inner
    return require_user_token_validator


def require_refresh_token(func):
    def inner(jsonT):
        token = (request.headers.get('Authorization'))
        if token is None:
            return {"Message": "Unauthorized Access"}, 401
        try:
            jwt.decode(
                    token, os.environ["refresh_token_key"],
                    algorithms=["HS256"]
                )
        except Exception:
            return {"Message": "Unauthorized Access"}, 401
        return func(jsonT)
    return inner
