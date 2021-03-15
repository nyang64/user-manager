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
from model.user_otp import UserOTPModel
# from utils.common import have_keys
from pytest_mock import MockerFixture
import flask
import json

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
    # def test_User_login_with_invalid_data(
    #         self, flask_app, mocker: MockerFixture):
    #     with flask_app.app_context():
    #         with flask_app.test_client() as client:
    #             resp = client.post('/v1/auth/token', json=dict(
    #                 email='1222',
    #                 password='12'
    #             ), follow_redirects=True)
    #             print(resp.data)
    #             assert resp.status_code == 400

    # def test_User_login_with_unregisterduser(
    #         self, flask_app, mocker: MockerFixture):
    #     with flask_app.app_context():
    #         with flask_app.test_client() as client:
    #             resp = client.post('/v1/auth/token', json=dict(
    #                 email='1222@gmail.com',
    #                 password='12'
    #             ), follow_redirects=True)
    #             print(resp.data)
    #             assert resp.status_code == 404

    # def test_User_login_with_incorrect_data(
    #         self, flask_app, mocker: MockerFixture):
    #     with flask_app.app_context():
    #         with flask_app.test_client() as client:
    #             resp = client.post('/v1/auth/token', json=dict(
    #                 email='esadmin@elementsci.com',
    #                 password='123'
    #             ), follow_redirects=True)
    #             print(resp.data)
    #             assert resp.status_code == 401

    # def test_User_login_with_valid_data(
    #         self, flask_app, mocker: MockerFixture):
    #     with flask_app.app_context():
    #         with flask_app.test_client() as client:
    #             resp = client.post('/v1/auth/token', json=dict(
    #                 email='esadmin@elementsci.com',
    #                 password='EleM3nTSci'
    #             ), follow_redirects=True)
    #             print(resp.data)
    #             assert resp.status_code == 200

    def test_update_password_with_valid_data(
            self, flask_app, mocker: MockerFixture):
        with flask_app.app_context():
            with flask_app.test_client() as client:
                mocker.patch(
                    jwt.require_user_token,
                    return_value=({}, {"user_role": ADMIN}))
                resp = client.put('/v1/updatepassword', json=dict(
                    email='esadmin@elementsci.com',
                    password='EleM3nTSci'
                ), follow_redirects=True)
                print(resp.data)
                assert resp.status_code == 200

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

    # def test_User_login_with_unregisterd_user(
    #         self, flask_app, auth_object, authdata_object):
    #     with flask_app.app_context():
    #         authdata_object.email = "yogendra_2667@gmail.com"
    #         authdata_object.password = "12345"
    #         with pytest.raises(Exception) as e:
    #             assert auth_object.User_login(authdata_object)
    #         assert str(e.value) == "404 Not Found: No Such User Exist"

    # def test_User_login_with_invalid_credentials(
    #         self, flask_app, auth_object, authdata_object):
    #     with flask_app.app_context():
    #         authdata_object.email = "yogendra.rai@infostretch.com"
    #         authdata_object.password = "1234511"
    #         with pytest.raises(Exception) as e:
    #             assert auth_object.User_login(authdata_object)
    #         assert str(e.value) == "401 Unauthorized: Invalid Credentials"

    # def test_User_login_with_valid_credentials(
    #         self, flask_app, auth_object, authdata_object):
    #     with flask_app.app_context():
    #         authdata_object.email = "yogendra.rai@infostretch.com"
    #         authdata_object.password = "12345"
    #         response_obj = auth_object.User_login(authdata_object)
    #         assert type(response_obj) is dict
    #         assert have_keys(
    #             response_obj,
    #             'id_token',
    #             'first_name',
    #             'last_name',
    #             'user_status',
    #             'isFirstTimeLogin',
    #             'message',
    #             'refresh_token') is True

    # # Test Cases For User_login End

    # # Test Cases For Refresh_token Start
    # def test_refresh_token(self, flask_app, auth_object, authdata_object):
    #     with flask_app.app_context():
    #         response_obj = auth_object.refresh_user_token(
    #             'yogendra.rai@gmail.com')
    #         assert type(response_obj) is dict
    #         assert have_keys(
    #             response_obj,
    #             'id_token',
    #             'isFirstTimeLogin',
    #             'message',
    #             'refresh_token') is True

    # # Test Cases For Refresh_token Start

    # # Test Cases For update Password Start

    # def test_update_password_unregisted_user(self, flask_app, auth_object):
    #     with flask_app.app_context():
    #         with pytest.raises(Exception) as e:
    #             assert auth_object.update_password(
    #                 'yogendra.rai@gmail.com',
    #                 '12345')
    #             assert str(e.value) == "404 Not Found: No Such User Exist"

    # def test_update_password_registed_user(self, flask_app, auth_object):
    #     with flask_app.app_context():
    #         with pytest.raises(Exception) as e:
    #             auth_obj = auth_object.update_password(
    #                 'yogendra.rai@infostretch.com',
    #                 '12345')
    #             assert (200 in auth_obj) is True
    #             assert (
    #                 {'message': 'Password Updated'} in auth_obj
    #                 ) is True
    #             if e is not None:
    #                 # To handel Database Max Pool Exception
    #                 assert ('500' in str(e.value)) is True
    # # Test Cases For update Password End

    # # Test Cases For Update OTP Start
    # def test_update_otp_unregisted_user(
    #         self, flask_app, auth_object, otp_not_exist_object):
    #     with flask_app.app_context():
    #         auth_object.update_otp_data(
    #             otp_not_exist_object)
    #         with pytest.raises(Exception) as e:
    #             assert auth_object.update_otp_data(
    #                 otp_not_exist_object)
    #             assert str(e.value) == "404 Not Found: No Such User Exist"

    # def test_update_otp_registed_user(
    #         self, flask_app, auth_object, otp_existing_object):
    #     with flask_app.app_context():
    #         with pytest.raises(Exception) as e:
    #             assert auth_object.update_otp_data(
    #                 otp_existing_object)
    #             assert str(e.value) == "404 Not Found: No Such User Exist"

    # # Test Cases For Send OTP END
