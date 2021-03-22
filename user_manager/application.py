from typing import Dict
from flask import Flask, jsonify, Response
from werkzeug.exceptions import BadRequest, HTTPException, Unauthorized,\
                    NotFound, Conflict, InternalServerError, MethodNotAllowed,\
                    Forbidden, NotAcceptable


class Appplication(Flask):
    def __init__(self, import_name, url_prefix):
        super().__init__(import_name)
        self.__add_routes()
        self.__allow_cors()
        self.__handle_errors()
        self._url_prefix = url_prefix

    def __add_routes(self):
        self.add_url_rule("/", 'index', self.__index, ['GET'])
        self.add_url_rule("/health-checkup", 'index', self.__index, ['GET'])

    def __index(self):
        return jsonify({"message": "ES API"})

    def __allow_cors(self):
        self.after_request(self.__add_cors_request)

    def __handle_errors(self):
        self.register_error_handler(BadRequest, self.__handle_bad_request)
        self.register_error_handler(Conflict, self.__handle_conflict)
        self.register_error_handler(NotFound, self.__handle_not_found)
        self.register_error_handler(Unauthorized, self.__handle_unauthorized)
        self.register_error_handler(Forbidden, self.__handle_forbidden)
        self.register_error_handler(NotAcceptable, self.__handle_not_accept)
        self.register_error_handler(MethodNotAllowed,
                                    self.__handle_method_not_allowed)
        self.register_error_handler(InternalServerError,
                                    self.__handle_internal_server_error)

    def __handle_not_accept(self, error: HTTPException):
        error_response = self.generate_response(
            error, f"Not Acceptable: '{error.description}'.")
        return jsonify(error_response), error.code

    def __handle_unauthorized(self, error: HTTPException):
        error_response = self.generate_response(
            error, f"Unauthorized: '{error.description}'.")
        return jsonify(error_response), error.code

    def __handle_forbidden(self, error: HTTPException):
        error_response = self.generate_response(
            error, f"Forbidden: '{error.description}'.")
        return jsonify(error_response), error.code

    def __handle_conflict(self, error: HTTPException):
        error_response = self.generate_response(
            error, f"request has error: '{error.description}'.")
        return jsonify(error_response), error.code

    def __handle_method_not_allowed(self, error: HTTPException):
        error_response = self.generate_response(
            error, f"request has error: '{error.description}'.")
        return jsonify(error_response), error.code

    def __handle_internal_server_error(self, error: HTTPException):
        error_response = self.generate_response(
            error, f"request has error: '{error.description}'.")
        return jsonify(error_response), error.code

    def __handle_not_found(self, error: HTTPException):
        error_response = self.generate_response(
            error, f"request has error: '{error.description}'.")
        return jsonify(error_response), error.code

    def __handle_bad_request(self, error: HTTPException):
        error_response = self.generate_response(
            error, f"request has error: '{error.description}'.")
        return jsonify(error_response), error.code

    @staticmethod
    def generate_response(error: HTTPException, detail: str) -> Dict:
        return {
            'errors': [{
                'status': str(error.code),
                'title': error.name,
                'detail': detail
            }]
        }

    def __add_cors_request(self, response: Response) -> Response:
        response.headers.add('Access-Control-Allow-Origin', "*")
        response.headers.add("Access-Control-Allow-Headers",
                             "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Methods",
                             "GET, POST, OPTIONS, PUT, DELETE")
        return response

    def register_blueprint(self, blueprint, **options):
        url_prefix = options.get('url_prefix', '')
        options['url_prefix'] = self._url_prefix + url_prefix
        super().register_blueprint(blueprint, **options)
