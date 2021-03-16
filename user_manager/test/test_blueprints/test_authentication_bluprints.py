from application import Appplication
from ma import ma
from config import get_connection_url
import pytest
from db import db
from flask_migrate import Migrate
from utils.constants import ADMIN
from utils import jwt
# from resources.authentication_manager import AuthOperation
# from model.user_registration import UserRegister
# from model.user_otp import UserOTPModel
# from utils.common import have_keys
from pytest_mock import MockerFixture
# import flask
# import json

from blueprint.auth_blueprint import AuthenticationBlueprint
from blueprint.user_blueprint import UserBluePrint
from blueprint.patient_blueprint import PatientBluePrint
from blueprint.provider_blueprint import ProviderBlueprint


def mock_require_user_token(*args):
    def require_user_token_validator(func):
        def inner(jsonT):
            print("jsc")
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


# @pytest.fixture
# def auth_object():
#     authObject = AuthOperation()
#     yield authObject


class TestClass:
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
                assert resp.status_code == 200

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
    # def test_update_password_with_valid_data(
    #         self, flask_app, mocker: MockerFixture):
    #     with flask_app.app_context():
    #         with flask_app.test_client() as client:
    #             mocker.patch(
    #                 jwt.require_user_token,
    #                 return_value=({}, {"user_role": ADMIN}))
    #             resp = client.put('/v1/updatepassword', json=dict(
    #                 email='esadmin@elementsci.com',
    #                 password='EleM3nTSci'
    #             ), follow_redirects=True)
    #             print(resp.data)
    #             assert resp.status_code == 200

    # def test_User_login_with_valid_data(
    #         self, flask_app, auth_object, mocker: MockerFixture):
    #     with flask_app.app_context():
    #         with flask_app.test_client() as client:
    #             client.get('/')
    #         with flask_app.test_request_context():
    #             request_mock = mocker.patch.object(flask, "request")

    #             # request_mock = mocker.patch(
    #             # 'resources.authentication_manager.AuthOperation')
    #             # jdata = {
    #             #     "email": "esadmin@elementsci.com",
    #             #     "password": "EleM3nTSci"
    #             #     }
    #             # request_mock.headers = {'content-type': 'application/json'}
    #             request_mock.get_json.return_value.email.return_value = "es"
    #             with pytest.raises(Exception) as e:
    #                 assert auth_object.login_user()
    #             print(e)
    #             assert "400 Bad Request" in str(e.value)
