from test.flask_app1 import create_test_app
from unittest import TestCase, mock

import os
import pytest
from db import db
from model.user_otp import UserOTPModel
from werkzeug.exceptions import InternalServerError


class TestOtpModel(TestCase):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

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

    def test_match_otp(self):
        app = create_test_app()
        with app.app_context():
            resp = UserOTPModel().matchOTP(1)
            self.assertIsNone(resp)

    def test_match_otp_raise_exception(self):
        app = create_test_app()
        with app.app_context():
            db.session.remove()
            db.drop_all()
            with pytest.raises(InternalServerError) as e:
                UserOTPModel().matchOTP(1)
            self.assertIsInstance(e.value, InternalServerError)

    def test_find_by_user_id(self):
        app = create_test_app()
        with app.app_context():
            resp = UserOTPModel().find_by_user_id(1)
            self.assertIsNone(resp)

    def test_find_by_user_id_raise_exception(self):
        app = create_test_app()
        with app.app_context():
            db.session.remove()
            db.drop_all()
            with pytest.raises(InternalServerError) as e:
                UserOTPModel().find_by_user_id(1)
            self.assertIsInstance(e.value, InternalServerError)

    def test_find_list_by_user_id(self):
        app = create_test_app()
        with app.app_context():
            patch = mock.patch.dict(os.environ, {"OTP_LIMIT_HOURS": "1",
                                             "OTP_LIMIT_MINUTES": "20"})
            patch.start()
            resp = UserOTPModel().find_list_by_user_id(1)
            self.assertEqual(0, resp)
            patch.stop()

    def test_find_list_by_user_id_raise_exception(self):
        app = create_test_app()
        with app.app_context():
            db.session.remove()
            db.drop_all()
            with pytest.raises(InternalServerError) as e:
                patch = mock.patch.dict(os.environ, {"OTP_LIMIT_HOURS": "1",
                                                 "OTP_LIMIT_MINUTES": "20"})
                patch.start()
                UserOTPModel().find_list_by_user_id(1)
                patch.stop()
            self.assertIsInstance(e.value, InternalServerError)

    def test_delete_all_otp_raise_exception(self):
        app = create_test_app()
        with app.app_context():
            db.session.remove()
            db.drop_all()
            with pytest.raises(InternalServerError) as e:
                UserOTPModel().deleteAll_OTP(1)
            self.assertIsInstance(e.value, InternalServerError)
