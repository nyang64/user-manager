from flask import Blueprint
from authentication.auth_services.authentication_manager import (
    AuthenticationManager
)


class AuthenticationBlueprint(Blueprint):
    def __init__(self):
        super().__init__(__class__.__name__, __name__)
        self.auth_obj = AuthenticationManager()
        self._add_routes()

    def _add_routes(self):
        self.add_url_rule('/register', 'Register User',
                          self.auth_obj.register_user,
                          methods=['POST'])
        self.add_url_rule('/auth/token', 'Get Token',
                          self.auth_obj.login_user,
                          methods=['POST'])
        self.add_url_rule('/updatepassword', 'Update user password',
                          self.auth_obj.update_user_password,
                          methods=['PUT'])
        self.add_url_rule('/refresh', 'Refresh Token',
                          self.auth_obj.refresh_access_token,
                          methods=['POST'])
        self.add_url_rule('/resetpassword', 'Reset Password',
                          self.auth_obj.reset_user_password,
                          methods=['PUT'])
