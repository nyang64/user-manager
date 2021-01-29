from flask import Blueprint
from authentication.auth_services.authentication_manager import AuthenticationManager


class AuthenticationBlueprint(Blueprint):
    def __init__(self):
        super().__init__(__class__.__name__, __name__)
        self.authObj = AuthenticationManager()
        self._add_routes()
         
    def _add_routes(self):
        self.add_url_rule('/register', 'Register User',
                          self.authObj.register_user,
                          methods=['POST'])
        self.add_url_rule('/auth/token', 'Get Token',
                          self.authObj.login_user,
                          methods=['POST'])
        self.add_url_rule('/updatepassword', 'Update user password',
                          self.authObj.update_user_password,
                          methods=['PUT'])
        self.add_url_rule('/refresh', 'Refresh Token',
                          self.authObj.refresh_access_token,
                          methods=['POST'])
        self.add_url_rule('/resetpassword', 'Reset Password',
                          self.authObj.reset_user_password,
                          methods=['PUT'])
        