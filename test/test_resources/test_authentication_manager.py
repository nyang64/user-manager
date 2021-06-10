import http
from datetime import datetime, timedelta
from test.flask_app1 import create_test_app
from unittest import TestCase, mock

from flask import request

import os
import pytest
from model.user_otp import UserOTPModel
from model.user_registration import UserRegister
from resources.authentication_manager import AuthOperation
from schema.login_schema import user_login_schema
from services.auth_services import AuthServices
from werkzeug.exceptions import BadRequest, InternalServerError


class TestAuthManager(TestCase):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.auth = AuthOperation()

    @mock.patch("resources.authentication_manager.request",  spec={})
    @mock.patch.object(AuthServices, "update_password")
    def test_update_user_password_for_incorrect_param(self, mock_pass, mock_req):
        decrypt = {"user_emal": "user@gmail.com"}
        app = create_test_app()
        mock_req.json = {"newpassword": "asd"}
        with app.test_request_context():
            resp = self.auth.update_user_password.__wrapped__(self.auth, decrypt)
            self.assertTupleEqual(resp, ({"Message": "Unauthorized Access"}, 401))

    @mock.patch("resources.authentication_manager.request", spec={})
    def test_update_user_password_raise_exception(self, mock_req):
        mock_req.json = {}
        decrypt = {"user_email": "user@gmail.com"}
        app = create_test_app()
        # Test to raise Internal Error
        with app.test_request_context():
            with pytest.raises(InternalServerError) as e:
                self.auth.update_user_password.__wrapped__(self.auth, decrypt)
            self.assertIsInstance(e.value, InternalServerError)

    @mock.patch.object(user_login_schema, "validate_data")
    @mock.patch.object(AuthServices, "User_login")
    def test_login_user(self, mock_auth, mock_schema):
        mock_auth.return_value = None
        mock_schema.return_value = None
        app = create_test_app()
        with app.test_request_context():
            resp = self.auth.login_user()
            self.assertIsNone(resp)

    @mock.patch.object(UserRegister, "find_by_email")
    @mock.patch("resources.authentication_manager.request", spec={})
    def test_reset_user_password_for_not_exist_user(self, mock_req, mock_user):
        mock_req.json = {"email": "user@gmail.com", "otp": "1212", "password": "AJ"}
        mock_user.return_value = None
        app = create_test_app()
        with app.test_request_context():
            resp = self.auth.reset_user_password()
            self.assertTupleEqual(resp, ({"message": "No Such User Exist"}, 404))

    @mock.patch.object(UserOTPModel, "matchOTP")
    @mock.patch.object(UserRegister, "find_by_email")
    @mock.patch("resources.authentication_manager.request", spec={})
    def test_reset_user_password_for_not_exist_otp(self, mock_req, mock_user, mock_otp):
        mock_req.json = {"email": "user@gmail.com", "otp": "1212", "password": "AJ"}
        mock_user.return_value = UserRegister(id=1)
        mock_otp.return_value = None
        app = create_test_app()
        with app.test_request_context():
            resp = self.auth.reset_user_password()
            self.assertTupleEqual(resp, ({"message": "OTP is Incorrect"}, 404))

    @mock.patch.object(UserOTPModel, "matchOTP")
    @mock.patch.object(UserRegister, "find_by_email")
    @mock.patch("resources.authentication_manager.request", spec={})
    def test_reset_user_password_for_incorrect_otp(self, mock_req, mock_user, mock_otp):
        mock_req.json = {"email": "user@gmail.com", "otp": "1212", "password": "AJ"}
        mock_user.return_value = UserRegister(id=1)
        mock_otp.return_value = UserOTPModel(otp="121")
        app = create_test_app()
        with app.test_request_context():
            resp = self.auth.reset_user_password()
            self.assertTupleEqual(resp, ({"message": "OTP is Incorrect"}, 404))

    @mock.patch.object(UserOTPModel, "matchOTP")
    @mock.patch.object(UserRegister, "find_by_email")
    @mock.patch("resources.authentication_manager.request", spec={})
    def test_reset_user_password_for_expired_otp(self, mock_req, mock_user, mock_otp):
        mock_req.json = {"email": "user@gmail.com", "otp": "1212", "password": "AJ"}
        mock_user.return_value = UserRegister(id=1)
        expire_time = datetime.now() - timedelta(days=3)
        mock_otp.return_value = UserOTPModel(otp="1212", created_at=expire_time)
        app = create_test_app()
        with app.test_request_context():
            patch = mock.patch.dict(os.environ, {"OTP_EXPIRATION_TIME_HOURS": "1",
                                                 "OTP_EXPIRATION_TIME_MINUTES": "20"})
            patch.start()
            resp = self.auth.reset_user_password()
            patch.stop()
            self.assertTupleEqual(resp, ({"message": "OTP is Expired"}, 410))

    @mock.patch.object(AuthServices, "update_otp_data")
    @mock.patch.object(UserOTPModel, "matchOTP")
    @mock.patch.object(UserRegister, "find_by_email")
    @mock.patch("resources.authentication_manager.request", spec={})
    def test_reset_user_password_(self, mock_req, mock_user, mock_otp, mock_update):
        mock_req.json = {"email": "user@gmail.com", "otp": "1212", "password": "AJ"}
        mock_user.return_value = UserRegister(id=1)
        mock_otp.return_value = UserOTPModel(otp="1212", created_at=datetime.now())
        mock_update.return_value = "updated"
        app = create_test_app()
        with app.test_request_context():
            patch = mock.patch.dict(os.environ, {"OTP_EXPIRATION_TIME_HOURS": "1",
                                                 "OTP_EXPIRATION_TIME_MINUTES": "20"})
            patch.start()
            resp = self.auth.reset_user_password()
            patch.stop()
            self.assertTupleEqual(resp, ({"message": "updated"}, 200))

    @mock.patch("resources.authentication_manager.request", spec={})
    def test_reset_user_password_for_incorrect_param(self, mock_req):
        mock_req.json = {"emil": "user@gmail.com"}
        app = create_test_app()
        with app.test_request_context():
            with pytest.raises(BadRequest) as e:
                self.auth.reset_user_password()
            self.assertIsInstance(e.value, BadRequest)

    @mock.patch.object(UserRegister, "find_by_email")
    @mock.patch("resources.authentication_manager.request", spec={})
    def test_reset_user_password_for_sending_otp_no_user_exist(
        self, mock_req, mock_user
    ):
        mock_req.json = {"email": "user@gmail.com"}
        mock_user.return_value = None
        app = create_test_app()
        with app.test_request_context():
            resp = self.auth.reset_user_password()
            self.assertTupleEqual(resp, ({"message": "No Such User Exist"}, 404))

    @mock.patch.object(UserOTPModel, "find_list_by_user_id")
    @mock.patch.object(UserRegister, "find_by_email")
    @mock.patch("resources.authentication_manager.request", spec={})
    def test_reset_user_password_for_sending_otp_limit_reached(
        self, mock_req, mock_user, mock_otp
    ):
        mock_req.json = {"email": "user@gmail.com"}
        mock_user.return_value = UserRegister(id=1)
        mock_otp.return_value = 2
        app = create_test_app()
        with app.test_request_context():
            patch = mock.patch.dict(os.environ, {"OTP_EXPIRATION_TIME_HOURS": "1",
                                                 "OTP_EXPIRATION_TIME_MINUTES": "20",
                                                 "OTP_LIMIT": "1"})
            patch.start()
            resp = self.auth.reset_user_password()
            patch.stop()
            self.assertTupleEqual(resp, ({"message": "OTP Limit Reached"}, 429))
