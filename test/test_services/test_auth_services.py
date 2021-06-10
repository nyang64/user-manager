from test.flask_app1 import create_test_app
from test.test_services.populate_data import PopulateData
from unittest import TestCase, mock

import os
import pytest
from db import db
from model.user_registration import UserRegister
from services.auth_services import AuthServices
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import Conflict, InternalServerError, NotFound, Unauthorized


class TestAuthServices(TestCase):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.auth_service = AuthServices()
        self.populate_data = PopulateData()

    def setUp(self):
        """Setting Up Database"""
        app = create_test_app()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Dropping all the database"""
        app = create_test_app()
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_new_user_duplicate_email(self):
        app = create_test_app()
        with app.app_context():
            self.populate_data.create_user("user@gmail.com")
            with pytest.raises(Conflict) as e:
                self.auth_service.register_new_user("user@gmail.com", "12")
            self.assertIsInstance(e.value, Conflict)

    @mock.patch.object(AuthServices, "flush_db")
    def test_register_new_user_raise_exception(self, mock_flush):
        mock_flush.side_effect = SQLAlchemyError("Error Occured")
        app = create_test_app()
        with app.app_context():
            with pytest.raises(InternalServerError) as e:
                self.auth_service.register_new_user("user@gmail.com", "")
            self.assertIsInstance(e.value, InternalServerError)

    def test_delete_regtration_for_none(self):
        app = create_test_app()
        with app.app_context():
            with pytest.raises(NotFound) as e:
                self.auth_service.delete_regtration(1)
            self.assertIsInstance(e.value, NotFound)

    @mock.patch.object(AuthServices, "save_db")
    def test_add_otp(self, mock_save):
        mock_save.return_value = None
        app = create_test_app()
        with app.app_context():
            self.auth_service.add_otp("1212")

    def test_refresh_user_token(self):
        app = create_test_app()
        with app.app_context():
            patch = mock.patch.dict(os.environ, {"ACCESS_TOKEN_KEY": "C718D5FDDEC279567385BE3E52894",
                                                 "REFRESH_TOKEN_KEY": "9EA72AD96C39A87A1AFF153983592"})
            patch.start()
            resp = self.auth_service.refresh_user_token("user@gmail.com")
            patch.stop()
            self.assertIsNotNone(resp)
            self.assertEqual(resp.get("message"), "Token Refreshed Successfully")

    def test_update_password(self):
        app = create_test_app()
        with app.app_context():
            auth = self.populate_data.register_user("register@gmail.com")
            self.populate_data.seed_otp_data(auth.id)
            resp = self.auth_service.update_password(auth.email, "newpass")
            self.assertTupleEqual(resp, ({"message": "Password Updated"}, 200))

    def test_update_password_raise_exception(self):
        app = create_test_app()
        with app.app_context():
            with pytest.raises(NotFound) as e:
                self.auth_service.update_password("user@fmai.com", "new")
            self.assertIsInstance(e.value, NotFound)

    @mock.patch.object(AuthServices, "update_db")
    def test_update_otp_data(self, mock_update):
        mock_update.return_value = None
        app = create_test_app()
        with app.app_context():
            resp = self.auth_service.update_otp_data("12")
            self.assertEqual("OTP Matched", resp)

    def test_user_login(self):
        u1 = UserRegister(email="user@gmail.com", password="password")
        app = create_test_app()
        with app.app_context():
            user = self.populate_data.create_user("user@gmail.com")
            self.populate_data.add_roles()
            self.populate_data.assign_role(user.id, 1)
            with pytest.raises(Exception) as e:
                self.auth_service.User_login(u1)
            self.assertIsInstance(e.value, Exception)

    def test_user_login_for_none_values(self):
        app = create_test_app()
        with app.app_context():
            self.populate_data.create_user("user@gmail.com")
            u = UserRegister(email="user1@gmail.com")
            with pytest.raises(NotFound) as e:
                self.auth_service.User_login(u)
            self.assertIsInstance(e.value, NotFound)

    def test_(self):
        app = create_test_app()
        with app.app_context():
            pass
