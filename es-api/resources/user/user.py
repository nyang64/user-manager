from flask_restful import Resource
from flask import request
from model.user_model import UserModel
from database.user import UserSchema


user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user = user_schema.load(user_json, session=tempSession)

        if UserModel.find_by_username(user.username):
            return {"message": "User Already Exist"}, 400

        user.save_to_db()

        return {"message": "User Created"}, 201
