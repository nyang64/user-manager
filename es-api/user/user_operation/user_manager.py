from werkzeug.exceptions import BadRequest, NotFound
from user.repository.user_repository import UserRepository
from utils.validation import validate_request, get_param, validate_number
from flask import jsonify, request
import http.client


class UserManager():
    def __init__(self):
        self.userObj = UserRepository()
        
    def create_user(self):
        request_data = validate_request()
        print('request_data', request_data)
        first_name, last_name, phone_number, email = self.__read_user_input(request_data)
        self.userObj.save_user(first_name, last_name, phone_number, email)
        return {'message' : 'User created', 'statusCode' : '201'}, http.client.CREATED
    
    def update_user(self, id):
        if id is None:
            raise BadRequest("parameter id is missing")
        request_data = validate_request()
        first_name, last_name, phone_number, email = self.__read_user_input(request_data)
        self.userObj.update_user_byid(id, first_name, last_name, phone_number, email)
        return {'message' : 'user updated', 'statusCode' : '200'}, http.client.OK
    
    def get_users(self):
        user_data = self.userObj.list_users()
        return {'data' : user_data, 'statusCode':'200'}, http.client.OK
    
    def delete_user(self, id):
        if id is None:
            raise BadRequest('')
        self.userObj.delete_user_byid(id)
        return {'message' : 'user updated', 'statusCode' : '202'}, http.client.ACCEPTED
    
    def get_detail_bytoken(self):
        resp = {
            'username' : 'mehul.sojitra@infostretch.com',
            'id':'122',
            'scope':'User',
            'status':'Active',
            'type':'Patient',
        }
        return jsonify(resp), http.client.OK
    

    def __read_user_input(self, request_data):
        first_name = get_param('first_name', 'missing parameter first_name is required', request_data)
        last_name = get_param('last_name', 'missing parameter last_name is required', request_data)
        phone_number = get_param('phone_number', 'missing parameter phone_number is required', request_data)
        email = get_param('email', 'missing parameter email is required', request_data) 
        
        validate_number(phone_number)
        if first_name is None or first_name == '':
            raise BadRequest('first_name cannot be None')
        if last_name is None or last_name == '':
            raise BadRequest('last_name cannot be None')
        if email is None or email == '':
            raise BadRequest('email cannot be None')
            
        return first_name, last_name, phone_number, email
    
    