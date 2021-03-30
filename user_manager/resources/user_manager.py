from werkzeug.exceptions import BadRequest
from flask import jsonify
import http.client
from services.user_services import UserServices
from schema.user_schema import create_user_schema, update_user_schema, UserSchema
from utils.validation import validate_request
from utils.jwt import require_user_token
from utils.constants import ADMIN, PROVIDER, PATIENT, ESUSER
from flask import request
from model.users import Users

users_schema = UserSchema(many=True)

class UserManager:
    def __init__(self):
        self.user_obj = UserServices()

    @require_user_token(ADMIN)
    def create_user(self, decrypt):
        request_data = validate_request()
        register, user = create_user_schema.load(request_data)
        user_id, user_uuid = self.user_obj.register_user(register, user)
        return {'message': 'User created and assigned role',
                'data': {
                    'user_uuid': user_uuid,
                    'user_id': user_id
                    },
                'status_code': '201'}, http.client.CREATED

    @require_user_token(ADMIN)
    def update_user(self, decrypt):
        user_id = request.args.get('id')
        if user_id is None:
            raise BadRequest("parameter id is missing")
        request_data = validate_request()
        first_name, last_name, phone_number = update_user_schema.load(
            request_data)
        self.user_obj.update_user_byid(user_id, first_name,
                                       last_name, phone_number)
        return {'message': 'user updated',
                'status_code': '200'}, http.client.OK

    def get_users(self):
        users = Users.all()

        return jsonify(users_schema.dump(users)), 200

    @require_user_token(ADMIN)
    def delete_user(self, decrypt):
        user_id = request.args.get('id')
        if user_id is None:
            raise BadRequest("parameter id is missing")
        self.user_obj.delete_user_byid(user_id)
        return {'message': 'user deleted',
                'status_code': '202'}, http.client.ACCEPTED

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

    @require_user_token(ADMIN, PROVIDER, PATIENT, ESUSER)
    def show(self, user_id):
        user = Users.find_by_id(user_id)
        user_schema = UserSchema()
        return user_schema.dump(user)

    @require_user_token(ADMIN, PROVIDER, PATIENT, ESUSER)
    def get_detail_bytoken(self, decrypt):
        email = decrypt.get('user_email')
        user = self.user_obj.get_detail_by_email(email)
        if user is None or len(user) < 3:
            return jsonify({'message': 'No data found'})
        resp = dict()
        resp['email'] = email
        resp['id'] = user[0]
        resp['uuid'] = user[1]
        resp['registration_id'] = user[2]
        resp['type'] = str(decrypt.get('user_role')).capitalize()
        resp['status'] = 'Active'
        resp['scope'] = 'User'
        return jsonify(resp), http.client.OK
