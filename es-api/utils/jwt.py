from flask import request
import jwt
import os
from utils.common import tokenTime


def encoded_Token(isrefreshToken: bool, user_email: str):
    if isrefreshToken:
        secret = os.environ["refresh_token_key"]
    else:
        secret = os.environ["access_token_key"]
    return jwt.encode({
                "user_email": user_email,
                "exp": (tokenTime(isrefreshToken))
                }, secret)


def require_user_token(func):
    def inner(jsonT):
        token = (request.headers.get('Authorization'))
        if token is None:
            return {"Message": "Unauthorized Access"}, 401
        try:
            deccrypted = jwt.decode(
                    token, os.environ["access_token_key"],
                    algorithms=["HS256"]
                )
        except jwt.ExpiredSignatureError:
            return {"Message": "Token is Expired"}

        except Exception as e:
            return {"Message": "Unauthorized Access"}, 401
        return func(jsonT, deccrypted)
    return inner


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
