from werkzeug.exceptions import BadRequest
from flask import jsonify
import http.client
import logging
from services.user_services import UserServices
from schema.user_schema import create_user_schema, update_user_schema, UserSchema
from utils.validation import validate_request
from utils.jwt import require_user_token
from utils.constants import ADMIN, PROVIDER, PATIENT, ESUSER
from flask import request
from model.users import Users
from utils.common import generate_random_password
from utils.send_mail import send_user_registration_email

users_schema = UserSchema(many=True)

class UserManager:
    def __init__(self):
        self.user_obj = UserServices()

    @require_user_token(ADMIN)
    def create_user(self, token):
        """
        Create a user in the system using the role provided and
        password in the request
        """
        request_data = validate_request()
        logging.debug(
            "User: {} with role: {} - is registering a new user : {}::{},  with role {}".format(token["user_email"],
                                                                                    token["user_role"],
                                                                                    request_data["first_name"],
                                                                                    request_data["last_name"],
                                                                                    request_data["role_name"]))

        # Set the password, if the password is not in the request
        if "password" not in request_data:
            pwd = generate_random_password()
            request_data["password"] = pwd

        register, user = create_user_schema.load(request_data)
        try:
            user_id, user_uuid = self.user_obj.register_user(register, user)

            send_user_registration_email(
                first_name=request_data["first_name"],
                last_name=request_data["last_name"],
                to_address=request_data["email"],
                username=request_data["email"],
                password= request_data["password"]
            )
            return {'message': 'User created and assigned role',
                    'data': {
                        'user_uuid': user_uuid,
                        'user_id': user_id
                        },
                    'status_code': '201'}, http.client.CREATED
        except Exception as error:
            logging.error(str(error))
            return {"message": "Error creating user: " + str(error)}, 404


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
        user_data = self.user_obj.list_users()
        return {'data': user_data,
                'status_code': '200'}, http.client.OK

    @require_user_token(ADMIN)
    def delete_user(self, decrypt):
        user_id = request.args.get('id')
        if user_id is None:
            raise BadRequest("parameter id is missing")
        self.user_obj.delete_user_byid(user_id)
        return {'message': 'user deleted',
                'status_code': '202'}, http.client.ACCEPTED

    @require_user_token(ADMIN, PROVIDER, PATIENT, ESUSER)
    def show(self, token):
        user_id = request.args.get('id')
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
