from werkzeug.exceptions import BadRequest, Conflict
from flask import jsonify
from datetime import datetime
import http.client
from user.repository.user_repository import UserRepository
from model.user_registration import UserRegister
from utils.validation import validate_request, get_param, validate_number


class UserManager():
    def __init__(self):
        self.userObj = UserRepository()

    def create_user(self):
        request_data = validate_request()
        print('request_data', request_data)
        register, user = self.__read_user_input(request_data)
        user_data = UserRegister(email=register[0],
                                 password=register[1])
        exist_user = UserRegister.find_by_username(register[0])
        if exist_user is not None:
            raise Conflict('user already exist')
        UserRegister.save_to_db(user_data)
        user_id = self.userObj.save_user(user[0], user[1],
                                         user[2], user_data.id)
        return {'message': 'User created',
                'data': user_id,
                'statusCode': '201'}, http.client.CREATED

    def update_user(self, id):
        if id is None:
            raise BadRequest("parameter id is missing")
        request_data = validate_request()
        first_name, last_name, phone_number, email = self.__read_update_input(
                                                        request_data)
        self.userObj.update_user_byid(id, first_name, last_name,
                                      phone_number, email)
        return {'message': 'user updated',
                'statusCode': '200'}, http.client.OK

    def get_users(self):
        user_data = self.userObj.list_users()
        return {'data': user_data,
                'statusCode': '200'}, http.client.OK

    def delete_user(self, id):
        if id is None:
            raise BadRequest('')
        self.userObj.delete_user_byid(id)
        return {'message': 'user deleted',
                'statusCode': '202'}, http.client.ACCEPTED

    def get_detail_bytoken(self):
        resp = {
            'email': 'mehul.sojitra@infostretch.com',
            'id': '122',
            'scope': 'User',
            'status': 'Active',
            'type': 'Patient',
            'uuid': '1f4ea346-25ce-4e35-a19c-22da1385997b'
        }
        return jsonify(resp), http.client.OK
    
    def __read_update_input(self, request_data):
        first_name = get_param('first_name', request_data)
        last_name = get_param('last_name', request_data)
        phone_number = get_param('phone_number', request_data)
        validate_number(phone_number)
        if first_name is None or first_name == '':
            raise BadRequest('first_name cannot be None')
        if last_name is None or last_name == '':
            raise BadRequest('last_name cannot be None')
        return first_name, last_name, phone_number, email

    def __read_user_input(self, request_data):
        email = get_param('email', request_data)
        password = get_param('password', request_data)
        first_name = get_param('first_name', request_data)
        last_name = get_param('last_name', request_data)
        phone_number = get_param('phone_number', request_data)
        validate_number(phone_number)
        if first_name is None or first_name == '':
            raise BadRequest('first_name cannot be None')
        if last_name is None or last_name == '':
            raise BadRequest('last_name cannot be None')
        if email is None or email == '':
            raise BadRequest('email cannot be None')
        register = (email, password)
        user = (first_name, last_name, phone_number)
        return register, user
