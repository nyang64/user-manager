from werkzeug.exceptions import BadRequest
from flask import request

def validate_request():
    if request.is_json:
        request_data = request.get_json()
    else:
        raise BadRequest('Invalid request. Excepted JSON')
    if not isinstance(request_data, dict):
        raise BadRequest('Invalid JSON request payload.')  
    return request_data

def get_param(name, request_data):
    if name in request_data:
        return request_data.get(name)
    else:
        raise BadRequest(f"'{name}' parameter is missing.")
    
def validate_number(phone_number):
    if phone_number is None:
        raise BadRequest('phone_number cannot be None')
    elif not phone_number.isdecimal():
        raise BadRequest('phone_number should be numeric')
    elif len(phone_number) != 10:
        raise BadRequest('Number less than 10 digit')