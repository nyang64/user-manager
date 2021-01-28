from typing import Dict
from flask import Flask, jsonify, Response
from werkzeug.exceptions import BadRequest, HTTPException, Unauthorized, NotFound, Conflict, InternalServerError, MethodNotAllowed

class Appplication(Flask):
    def __init__(self, _name):
        super().__init__(_name)
        self.__allow_cors()
        self.__handle_errors()
        
    def __allow_cors(self):
        self.after_request(self.__add_cors_request)
    
    def __handle_errors(self):
        self.register_error_handler(BadRequest, self.__handle_bad_request)
        self.register_error_handler(NotFound, self.__handle_not_found)
        self.register_error_handler(MethodNotAllowed, self.__handle_method_not_allowed)
        self.register_error_handler(InternalServerError, self.__handle_internal_server_error)
        
    def __handle_method_not_allowed(self, error: HTTPException):
        print(error)
        error_response = self.generate_response(error, f"request has error: '{error.description}'.")
        return jsonify(error_response), error.code
        
    def __handle_internal_server_error(self, error: HTTPException):
        print(error)
        error_response = self.generate_response(error, f"request has error: '{error.description}'.")
        return jsonify(error_response), error.code
    
    def __handle_not_found(self, error: HTTPException):
        error_response = self.generate_response(error, f"request has error: '{error.description}'.")
        return jsonify(error_response), error.code
        
    def __handle_bad_request(self, error: HTTPException):
        error_response = self.generate_response(error, f"request has error: '{error.description}'.")
        return jsonify(error_response), error.code
    
    @staticmethod    
    def generate_response(error: HTTPException, detail: str)-> Dict:
        return {
            'errors': [{
                'status': str(error.code),
                'title': error.name,
                'detail': detail
            }]
        }
        
        
    def __add_cors_request(self, response: Response)-> Response:
        response.headers.add('Access-Control-Allow-Origin', "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, DELETE")
        return response