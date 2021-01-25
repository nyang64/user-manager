from flask import request
import jwt
# import datetime


def require_user_token(func):
    def inner(jsonT):
        pep = (request.headers.get('Authorization'))
        if pep is None:
            return {"Message": "Unauthorized Access"}, 401
        try:
            jwt.decode(
                    pep, "C718D5FDDEC279567385BE3E52894", algorithms=["HS256"]
                )
            # print(dec["exp"])
            # print("uTT",int(dec["exp"]))
            # print("uTN",datetime.datetime.now().timestamp())
            # if int(dec["exp"]) < datetime.datetime.now().timestamp():
            #     return {"Message": "Token Expired"}, 401
            # return func(jsonT)
        except Exception as e:
            print(e)
            return {"Message": "Unauthorized Access"}, 401
        return func(jsonT)
    return inner


def require_refresh_token(func):
    def inner(jsonT):
        pep = (request.headers.get('Authorization'))
        if pep is None:
            return {"Message": "Unauthorized Access"}, 401
        try:
            jwt.decode(
                    pep, "9EA72AD96C39A87A1AFF153983592", algorithms=["HS256"]
                )
            # print(dec["exp"])
            # print("uTT",int(dec["exp"]))
            # print("uTN",datetime.datetime.now().timestamp())
            # if int(dec["exp"]) < datetime.datetime.now().timestamp():
            #     return {"Message": "Token Expired"}, 401
            # return func(jsonT)
        except Exception as e:
            print(e)
            return {"Message": "Unauthorized Access"}, 401
        return func(jsonT)
    return inner
