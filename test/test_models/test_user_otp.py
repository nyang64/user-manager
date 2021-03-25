import pytest
from model.user_otp import UserOTPModel
from application import Appplication
from config import get_connection_url
from flask_migrate import Migrate
from db import db
from ma import ma


@pytest.fixture
def flask_app():
    app = Appplication(__name__, '/v1')
    app.config["SQLALCHEMY_DATABASE_URI"] = get_connection_url()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config["E_EXCEPTIONS"] = True
    app.config["TESTING"] = True
    migrate = Migrate()
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    yield app


class TestUserOtpModel:
    def test_user_otp_schema(self, flask_app):
        with flask_app.app_context():
            UserOTPModel.matchOTP(None, None)

    def test_user_otp_delete(self, flask_app):
        with flask_app.app_context():
            UserOTPModel.deleteAll_OTP(None)

    def test_user_otp_find_by_id(self, flask_app):
        with flask_app.app_context():
            UserOTPModel.find_by_user_id(None)

    def test_user_otp_find_list_by_id(self, flask_app):
        with flask_app.app_context():
            UserOTPModel.find_list_by_user_id(None)
