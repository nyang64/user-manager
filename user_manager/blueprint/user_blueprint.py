from flask import Blueprint
from resources.user_manager import UserManager


class UserBluePrint(Blueprint):
    def __init__(self):
        super().__init__(__class__.__name__, __name__)
        self.userObj = UserManager()
        self._add_routes()

    def _add_routes(self):
        self.add_url_rule('/create/user',
                          'create users',
                          self.userObj.create_user,
                          methods=['POST'])
        self.add_url_rule('/user',
                          'Update users',
                          self.userObj.update_user,
                          methods=['PUT'])
        self.add_url_rule('/users',
                          'List users',
                          self.userObj.get_users,
                          methods=['GET'])
        self.add_url_rule('/users/role',
                          'List users by role',
                          self.userObj.get_users_by_role,
                          methods=['GET'])
        self.add_url_rule('/user',
                          'Delete users',
                          self.userObj.delete_user,
                          methods=['DELETE'])
        self.add_url_rule('/user/get',
                          'user information by token',
                          self.userObj.get_detail_bytoken,
                          methods=['GET'])
        self.add_url_rule('/user/details',
                          'show user by id',
                          self.userObj.show,
                          methods=['GET'])
        self.add_url_rule('/users/role',
                          'show user by id',
                          self.userObj.show,
                          methods=['GET'])
