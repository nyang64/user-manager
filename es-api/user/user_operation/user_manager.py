from werkzeug.exceptions import BadRequest, Conflict
from flask import jsonify
import http.client
from user.repository.user_repository import UserRepository
from model.user_registration import UserRegister
from user.schema.user_schema import create_user_schema, update_user_schema
from utils.validation import validate_request, get_param, validate_number
from common.common_repo import CommonRepo
from utils.common import encPass
from utils.jwt import require_user_token
from utils.constants import ADMIN, PROVIDER, PATIENT, ESUser
from flask import request


class UserManager():
    def __init__(self):
        self.userObj = UserRepository()
        self.commonObj = CommonRepo()
    
    @require_user_token(ADMIN)
    def create_user(self, decrypt):
        request_data = validate_request()
        register, user = create_user_schema.load(request_data)
        self.commonObj.is_email_registered(register[0])
        user_data = UserRegister(email=register[0],
                                 password=encPass(register[1]))
        UserRegister.save_db(user_data)
        user_id, user_uuid = self.userObj.save_user(user[0], user[1],
                                                    user[2], user_data.id)
        self.userObj.assign_user_role(user_id)
        return {'message': 'User created and assigned role',
                'data': user_uuid,
                'statusCode': '201'}, http.client.CREATED

    @require_user_token(ADMIN)
    def update_user(self, decrypt):
        user_id = request.args.get('id')
        if user_id is None:
            raise BadRequest("parameter id is missing")
        request_data = validate_request()
        first_name, last_name, phone_number = update_user_schema.load(
            request_data)
        self.userObj.update_user_byid(user_id, first_name,
                                      last_name, phone_number)
        return {'message': 'user updated',
                'statusCode': '200'}, http.client.OK

    def get_users(self):
        user_data = self.userObj.list_users()
        return {'data': user_data,
                'statusCode': '200'}, http.client.OK

    @require_user_token(ADMIN)
    def delete_user(self, decrypt):
        user_id = request.args.get('id')
        if user_id is None:
            raise BadRequest("parameter id is missing")
        self.userObj.delete_user_byid(user_id)
        return {'message': 'user deleted',
                'statusCode': '202'}, http.client.ACCEPTED

    def mock_get_detail_bytoken(self):
        resp = {
            'email': 'mehul.sojitra@infostretch.com',
            'id': '122',
            'scope': 'User',
            'status': 'Active',
            'type': 'Patient',
            'uuid': '1f4ea346-25ce-4e35-a19c-22da1385997b'
        }
        return jsonify(resp), http.client.OK

    @require_user_token(ADMIN, PROVIDER, PATIENT, ESUser)
    def get_detail_bytoken(self, decrypt):
        print(decrypt)
        email = decrypt.get('user_email')
        self.commonObj.get_detail_by_email(email)
        return jsonify({}), http.client.OK
