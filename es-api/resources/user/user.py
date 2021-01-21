from flask_restful import Resource
from flask import request
from model.user_model import UserModel
from database.user import UserSchema
from utils.common import *
from utils.jwt import *
import datetime
import jwt
user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        #user = user_schema.load(user_json, session=tempSession)
        print('user', user_json)
        ''' if UserModel.find_by_username(user.username):
            return {"message": "User Already Exist"}, 400

        user.save_to_db() '''

        return {"message": "User Created"}, 201



class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        if have_keys(user_json,'username','password') is False:
            return {"message": "Invalid Request Parameters"},200
        udt = UserModel.find_by_username(user_json["username"])
        if udt is None:
            return {"message": "Invalid Credentials"},401
        if udt.password == user_json["password"]:
            encoded_jwt = jwt.encode({"username": user_json["username"],"exp":(tokenTime()), }, "TestSecret")
            # print("tkn", jwt.decode(encoded_jwt, "TestSecret", algorithms=["HS256"]))
            return {"message" : "Successfully Login","id_token" : encoded_jwt },200
        return {"message": "Invalid Credentials"},200

class UserResetPassword(Resource):
    @classmethod
    @require_user_token
    def post(cls):
        user_json = request.get_json()
        if have_keys(user_json,'username','oldpassword','newpassword') is False:
            return {"message": "Invalid Request Parameters"},200
        dt = UserModel.find_by_username(username=user_json["username"])
        if dt == None:
            return {"message": "No Such User Exist"}
        if dt.password != user_json["oldpassword"]:
            return {"message": "Incorrect Password"}
        if user_json["newpassword"] == None or user_json["newpassword"] == "":
            return {"message": "New password does not meet minimum criteria"}
        dt.password=user_json["newpassword"]
        dt.update_db()
        return {"message":"Password Updated"}
