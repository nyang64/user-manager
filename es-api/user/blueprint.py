from flask import Blueprint
from user.user_operation.user_manager import UserManager

class UserBluePrint(Blueprint):
    def __init__(self):
        super().__init__(__class__.__name__, __name__)
        self.userObj = UserManager()
        self._add_routes()
        
    def _add_routes(self):
        self.add_url_rule('/users', 'create users', self.userObj.create_user, methods=['POST'])