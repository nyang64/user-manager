from flask import Blueprint
from authentication.operation.authentication_operation import (
    AuthOperation
)


class AuthenticationBlueprint(Blueprint):
    def __init__(self):
        super().__init__(__class__.__name__, __name__)
        self.auth_login = AuthOperation()
        self._add_routes()

    def _add_routes(self):
        self.add_url_rule('/auth/token', 'Get Token',
                          self.auth_login.login_user,
                          methods=['POST'])
        self.add_url_rule('/updatepassword', 'Update user password',
                          self.auth_login.update_user_password,
                          methods=['PUT'])
        self.add_url_rule('/refresh', 'Refresh Token',
                          self.auth_login.refresh_token,
                          methods=['POST'])
        self.add_url_rule('/resetpassword', 'Reset Password',
                          self.auth_login.reset_user_password,
                          methods=['PUT'])
