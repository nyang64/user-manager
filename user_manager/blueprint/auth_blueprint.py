from flask import Blueprint
from resources.authentication_manager import (
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
        self.add_url_rule('/setpassword', 'Set known password',
                          self.auth_login.update_and_email_set_password,
                          methods=['POST'])
        self.add_url_rule('/refresh', 'Refresh Token',
                          self.auth_login.refresh_token,
                          methods=['POST'])
        self.add_url_rule('/refresh_user_token', 'Refresh User Token',
                          self.auth_login.user_refresh_token,
                          methods=['POST'])
        self.add_url_rule('/resetpassword', 'Reset Password',
                          self.auth_login.reset_user_password,
                          methods=['PUT'])
        self.add_url_rule('/logout', 'Logout',
                          self.auth_login.delete,
                          methods=['DELETE'])
        self.add_url_rule('/validate_token', 'Validate Token',
                          self.auth_login.validate_token,
                          methods=['POST'])
        self.add_url_rule('/unlock_account', 'Unlock User Account',
                          self.auth_login.unlock_account,
                          methods=['POST'])
        self.add_url_rule('/patients/portal_login', 'Verify Patient for login',
                          self.auth_login.patient_portal_login,
                          methods=['POST'])
