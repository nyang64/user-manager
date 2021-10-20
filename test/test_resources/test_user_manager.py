import http
from test.flask_app1 import create_test_app
from unittest import TestCase, mock

import pytest
from resources.user_manager import UserManager
from services.user_services import UserServices
from werkzeug.exceptions import BadRequest


class TestUserManager(TestCase):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.user = UserManager()

    @mock.patch.object(UserServices, "register_user")
    @mock.patch("resources.user_manager.send_user_registration_email")
    @mock.patch("utils.validation.request", spec={})
    def test_create_user(self, request, mock_email, mock_user):
        reqdata = {
            "email": "avilash@gmail.com",
            "password": "test1234",
            "first_name": "Avi",
            "last_name": "Jha",
            "phone_number": "8097865432",
            "role_name": "PROVIDER",
        }
        request.is_json = True
        request.json = reqdata
        expected_resp = (
            {
                "message": "User created and assigned role",
                "data": {"user_uuid": "1212", "user_id": "1"},
                "status_code": "201",
            },
            http.client.CREATED,
        )
        app = create_test_app()
        with app.test_request_context():
            mock_user.return_value = "1", "1212"
            args = {"user_role": "R", "user_email": "E"}
            resp = UserManager.create_user.__wrapped__(self.user, args)
            self.assertEqual(resp, expected_resp)

    @mock.patch.object(UserServices, "update_user_byid")
    @mock.patch("utils.validation.request", spec={})
    @mock.patch("resources.user_manager.request", spec={})
    def test_update_user(self, request, request1, mock_user):
        request.args = {"id": 1}
        reqdata = {
            "first_name": "avilash-updates-5",
            "last_name": "5frb",
            "phone_number": "9988776655",
        }
        request1.is_json = True
        request1.json = reqdata
        expected_resp = (
            {"message": "user updated", "status_code": "200"},
            http.client.OK,
        )
        app = create_test_app()
        with app.test_request_context():
            mock_user.return_value = None
            resp = UserManager.update_user.__wrapped__(self.user, "")
            self.assertEqual(resp, expected_resp)

    def test_update_user_for_none(self):
        app = create_test_app()
        with app.test_request_context():
            with pytest.raises(BadRequest) as e:
                UserManager.update_user.__wrapped__(self.user, "")
            self.assertIsInstance(e.value, BadRequest)

    @mock.patch.object(UserServices, "delete_user_byid")
    @mock.patch("resources.user_manager.request", spec={})
    def test_delete_user(self, request, mock_user):
        request.args = {"id": 1}
        expected_resp = (
            {"message": "user deleted", "status_code": "202"},
            http.client.ACCEPTED,
        )
        app = create_test_app()
        with app.test_request_context():
            mock_user.return_value = None
            resp = UserManager.delete_user.__wrapped__(self.user, "")
            self.assertEqual(resp, expected_resp)

    def test_delete_user_for_none(self):
        app = create_test_app()
        with app.test_request_context():
            with pytest.raises(BadRequest) as e:
                UserManager.delete_user.__wrapped__(self.user, "")
            self.assertIsInstance(e.value, BadRequest)

    @mock.patch.object(UserServices, "list_users")
    def test_get_user_for_none(self, mock_user):
        app = create_test_app()
        mock_user.return_value = None
        with app.test_request_context():
            resp = UserManager.get_users(self.user)
            self.assertIsNotNone(resp)

    @mock.patch.object(UserServices, "get_detail_by_email")
    def test_get_detail_by_token(self, mock_user):
        app = create_test_app()
        args = {"user_role": "R", "user_email": "E"}
        mock_user.return_value = [1, 2, 3]
        with app.test_request_context():
            resp = UserManager.get_detail_bytoken.__wrapped__(self.user, args)
            self.assertEqual(resp[1], http.client.OK)

    @mock.patch.object(UserServices, "get_detail_by_email")
    def test_get_detail_by_token_for_none(self, mock_user):
        app = create_test_app()
        args = {"user_role": "R", "user_email": "E"}
        mock_user.return_value = None
        with app.test_request_context():
            resp = UserManager.get_detail_bytoken.__wrapped__(self.user, args)
            self.assertEqual(resp.json, {"message": "No data found"})
