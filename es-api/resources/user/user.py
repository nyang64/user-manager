from flask_restful import Resource
from flask import request
from model.user_model import UserModel
from database.user import UserSchema
from utils.common import *
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
            return {"message": "Invalid Request Parameters"}
        udt = UserModel.find_by_username(user_json["username"])
        if udt is None:
            return {"message": "Invalid Credentials"}
        if udt.password == user_json["password"]:
            encoded_jwt = jwt.encode({"username": user_json["username"],"exp":tokenTime()}, "TestSecret")
            # print("tkn", jwt.decode(encoded_jwt, "TestSecret", algorithms=["HS256"]))
            return {"message" : "Successfully Login","token" : encoded_jwt }
        return {"message": "Invalid Credentials"}
