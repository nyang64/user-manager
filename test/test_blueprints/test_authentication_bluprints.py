from application import Appplication
from ma import ma
from config import get_connection_url
import pytest
from db import db
from flask_migrate import Migrate
from utils.constants import ADMIN
from utils import jwt
from pytest_mock import MockerFixture
from blueprint.auth_blueprint import AuthenticationBlueprint
from blueprint.user_blueprint import UserBluePrint
from blueprint.patient_blueprint import PatientBluePrint
from blueprint.provider_blueprint import ProviderBlueprint
import os
from werkzeug.datastructures import Headers


def mock_require_user_token(*args):
    def require_user_token_validator(func):
        def inner(jsonT):
            decrypted = {"user_role": ADMIN}
            return func(jsonT, decrypted)
        return inner
    return require_user_token_validator


def init_require_user_toke():
    jwt.require_user_token = mock_require_user_token()


@pytest.fixture
def flask_app():
    init_require_user_toke()
    app = Appplication(__name__, '/v1')
    app.config["SQLALCHEMY_DATABASE_URI"] = get_connection_url()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config["E_EXCEPTIONS"] = True
    app.config["TESTING"] = True
    migrate = Migrate()
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    auth_blueprint = AuthenticationBlueprint()
    app.register_blueprint(auth_blueprint)

    user_blueprint = UserBluePrint()
    app.register_blueprint(user_blueprint)

    provider_blueprint = ProviderBlueprint()
    app.register_blueprint(provider_blueprint)

    patient_blueprint = PatientBluePrint()
    app.register_blueprint(patient_blueprint)

    yield app


class TestAuthenticationBluePrint:
    # Test Cases For User_login Start
    def test_User_login_with_invalid_data(
            self, flask_app, mocker: MockerFixture):
        with flask_app.app_context():
            with flask_app.test_client() as client:
                resp = client.post('/v1/auth/token', json=dict(
                    email='1222',
                    password='12'
                ), follow_redirects=True)
                assert resp.status_code == 400

    def test_User_login_with_unregisterduser(
            self, flask_app, mocker: MockerFixture):
        with flask_app.app_context():
            with flask_app.test_client() as client:
                resp = client.post('/v1/auth/token', json=dict(
                    email='1222@gmail.com',
                    password='12'
                ), follow_redirects=True)
                assert resp.status_code == 404

    def test_User_login_with_incorrect_data(
            self, flask_app, mocker: MockerFixture):
        with flask_app.app_context():
            with flask_app.test_client() as client:
                resp = client.post('/v1/auth/token', json=dict(
                    email='esadmin@elementsci.com',
                    password='123'
                ), follow_redirects=True)
                assert resp.status_code == 401

    def test_User_login_with_valid_data(
            self, flask_app, mocker: MockerFixture):
        with flask_app.app_context():
            with flask_app.test_client() as client:
                resp = client.post('/v1/auth/token', json=dict(
                    email='esadmin@elementsci.com',
                    password='EleM3nTSci'
                ), follow_redirects=True)
                os.environ["test_token"] = resp.json["id_token"]
                os.environ["test_refresh_token"] = resp.json["refresh_token"]
                assert resp.status_code == 200

    # Test Cases For User_login End

    # Test Cases For User_Reset_Password Start
    def test_User_reset_password_exist(
            self, flask_app, mocker: MockerFixture):
        with flask_app.app_context():
            with flask_app.test_client() as client:
                resp = client.put('/v1/resetpassword', json=dict(
                    email='esadmin@elementsci.com',
                ), follow_redirects=True)
                assert resp.status_code == 200

    def test_User_reset_password_no_such_user(
            self, flask_app, mocker: MockerFixture):
        with flask_app.app_context():
            with flask_app.test_client() as client:
                resp = client.put('/v1/resetpassword', json=dict(
                    email='abc@gbc.com'
                ), follow_redirects=True)
                assert resp.status_code == 404

    def test_User_reset_password_without_params(
            self, flask_app, mocker: MockerFixture):
        with flask_app.app_context():
            with flask_app.test_client() as client:
                resp = client.put('/v1/resetpassword', json=dict(
                ), follow_redirects=True)
                assert resp.status_code == 400

    def test_User_reset_password_without_match_otp_no_user(
            self, flask_app, mocker: MockerFixture):
        with flask_app.app_context():
            with flask_app.test_client() as client:
                resp = client.put('/v1/resetpassword', json=dict(
                      email='abc@gbc.com',
                      otp='1234',
                      password='12345678'
                ), follow_redirects=True)
                assert resp.status_code == 404

    def test_User_reset_password_without_match_otp_valid_user(
            self, flask_app, mocker: MockerFixture):
        with flask_app.app_context():
            with flask_app.test_client() as client:
                resp = client.put('/v1/resetpassword', json=dict(
                      email='esadmin@elementsci.com',
                      otp='1234',
                      password='12345678'
                ), follow_redirects=True)
                assert resp.status_code == 404

    # Test Cases For User_Reset_Password End

    # Test Cases For User_Refresh_Token Start
    def test_User_refresh_token(
            self, flask_app, mocker: MockerFixture):
        with flask_app.app_context():
            test_token = os.environ["test_refresh_token"]
            header = Headers(
                {
                    'Authorization': test_token
                })
            with flask_app.test_client() as client:
                resp = client.post(
                    '/v1/refresh',
                    headers=header,
                    follow_redirects=True)
                assert resp.status_code == 200

    # Test Cases For User_Refresh_Token End

    def test_update_password_with_valid_data(
            self, flask_app, mocker: MockerFixture):
        with flask_app.app_context():
            test_token = os.environ["test_token"]
            header = Headers(
                {
                    'Authorization': test_token
                })
            with flask_app.test_client() as client:
                resp = client.put(
                    '/v1/updatepassword',
                    headers=header,
                    follow_redirects=True,
                    json=dict(
                        email='esadmin@elementsci.com',
                        newpassword="EleM3nTSci"
                        ))
                assert resp.status_code == 200

    def test_update_password_with_invalid_data(
            self, flask_app, mocker: MockerFixture):
        with flask_app.app_context():
            test_token = os.environ["test_token"]
            header = Headers(
                {
                    'Authorization': test_token
                })
            with flask_app.test_client() as client:
                resp = client.put(
                    '/v1/updatepassword',
                    headers=header,
                    follow_redirects=True,
                    json=dict(
                        email='esadmin@elementsci.com'
                        ))
                assert resp.status_code == 500