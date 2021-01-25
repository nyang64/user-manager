from flask_restful import Resource
from flask import request
from model.user_model import UserModel
from database.user import UserSchema
from utils.common import have_keys, tokenTime
from utils.jwt import require_user_token, require_refresh_token
# import datetime
import jwt
user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        if have_keys(user_json, 'id', 'username', 'password') is False:
            return {"message": "Invalid Request Parameters"}, 200
        if UserModel.find_by_username(user_json["username"]):
            return {"message": "User Already Exist"}, 400

        user = UserModel(
            user_json['id'],
            user_json["username"], user_json["password"], 1, 1, 1
            )
        user.save_to_db()

        return {"message": "User Created"}, 201


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        if have_keys(user_json, 'username', 'password') is False:
            return {"message": "Invalid Request Parameters"}, 200
        udt = UserModel.find_by_username(user_json["username"])
        if udt is None:
            return {"message": "No Such User Exist"}, 404
        if udt.password == user_json["password"]:
            encoded_accessToken = jwt.encode({
                "username": user_json["username"],
                "exp": (tokenTime(False))
                }, "C718D5FDDEC279567385BE3E52894")
            encoded_refreshToken = jwt.encode({
                "username": user_json["username"],
                "exp": (tokenTime(True))
                 }, "9EA72AD96C39A87A1AFF153983592")

            return {
                "message": "Successfully Login",
                "id_token": encoded_accessToken,
                "refresh_token": encoded_refreshToken
                }, 200
        return {"message": "Invalid Credentials"}, 401


class UpdateUserPassword(Resource):
    @classmethod
    @require_user_token
    def put(cls):
        user_json = request.get_json()
        have_key = have_keys(
            user_json, 'username',
            'oldpassword', 'newpassword'
         )
        if have_key is False:
            return {"message": "Invalid Request Parameters"}, 200
        dt = UserModel.find_by_username(username=user_json["username"])
        if dt is None:
            return {"message": "No Such User Exist"}, 404
        if dt.password != user_json["oldpassword"]:
            return {"message": "Incorrect Password"}, 200
        if user_json["newpassword"] is None or user_json["newpassword"] == "":
            return {
                "message": "New password does not meet minimum criteria"
                }, 200
        dt.password = user_json["newpassword"]
        dt.update_db()
        return {"message": "Password Updated"}, 200


class ResetUserPassword(Resource):
    @classmethod
    @require_user_token
    def put(cls):
        user_json = request.get_json()
        have_key = have_keys(
            user_json, 'username', 'otp'
            # 'oldpassword', 'newpassword'
         )
        if have_key is False:
            return {"message": "Invalid Request Parameters"}, 200
        dt = UserModel.find_by_username(username=user_json["username"])
        if dt is None:
            return {"message": "No Such User Exist"}, 404
        return {"message": "OTP Sent to Email"}, 200


class refreshAccessToken(Resource):
    @classmethod
    @require_refresh_token
    def post(cls):
        user_json = request.get_json()
        have_key = have_keys(
            user_json, 'username'
         )
        if have_key is False:
            return {"message": "Invalid Request Parameters"}, 200
        encoded_accessToken = jwt.encode({
            "username": user_json["username"],
            "exp": (tokenTime(False))
            }, "C718D5FDDEC279567385BE3E52894")
        return {
                "message": "Token Generated Successfully",
                "id_token": encoded_accessToken
                }, 200


# 200 -> Successful
# 404 -> User doesn't exist
# 401 -> Unauthorized
