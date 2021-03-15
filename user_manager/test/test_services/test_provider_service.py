from application import Appplication
from ma import ma
from config import get_connection_url
import pytest
from db import db
from flask_migrate import Migrate
# from utils.constants import ADMIN
# from utils import jwt
# from utils.common import generateOTP
from services.provider_services import ProviderService
from services.auth_services import AuthServices
from model.user_registration import UserRegister
# from schema.provider_schema import CreateProviderSchema
# # from utils.common import have_keys
# import json

# def mock_require_user_token(*args):
#     def require_user_token_validator(func):
#         def inner(jsonT):
#             print("jsc")
#             decrypted = {"user_role": ADMIN}
#             return func(jsonT, decrypted)
#         return inner
#     return require_user_token_validator


# def init_require_user_toke():
#     jwt.require_user_token = mock_require_user_token


@pytest.fixture
def flask_app():
    # init_require_user_toke()
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


@pytest.fixture
def provider_object():
    providerObject = ProviderService()
    yield providerObject


@pytest.fixture
def auth_object():
    authObject = AuthServices()
    yield authObject


@pytest.fixture
def provider_schema_object():
    register = ("yug.rai"+'101'+"@infostretch.com", "12345")
    user = ("yogi1", "rai1", "9999999999")
    provider = "1"
    yield register, user, provider


# @pytest.fixture
# def provider_exsisting_schema_object():
#     register = ("yug.rai@infostretch.com", "12345")
#     user = ("yogi1", "rai1", "9999999999")
#     provider = "1"
#     yield register, user, provider


class TestClass:
    # Test Cases For Provider Register Start

    # def test_provider_register_with_none_data(
    #         self,
    #         flask_app,
    #         provider_object):
    #     with flask_app.app_context():
    #         with pytest.raises(Exception) as e:
    #             register = ("", "")
    #             user = ("", "")
    #             provider = ""
    #             response = provider_object.register_provider(
    #                     register,
    #                     user,
    #                     provider
    #                     )
    #             assert response is True
    #         assert "400 Bad Request" in str(e.value)

    def test_provider_register_with_valid_data(
            self,
            flask_app,
            provider_object,
            provider_schema_object):

        with flask_app.app_context():
            response = provider_object.register_provider(
                    provider_schema_object[0],
                    provider_schema_object[1],
                    provider_schema_object[2]
                    )
            assert response is True

    def test_provider_register_with_existing_data(
            self,
            flask_app,
            provider_object,
            provider_schema_object):

        with flask_app.app_context():
            with pytest.raises(Exception) as e:
                response = provider_object.register_provider(
                        provider_schema_object[0],
                        provider_schema_object[1],
                        provider_schema_object[2]
                        )
                assert response is True
            assert "409 Conflict" in str(e.value)

    # Test Cases For Send OTP END
    def test_delete_provider(
            self,
            flask_app,
            auth_object,
            provider_schema_object):
        with flask_app.app_context():
            user_obj = UserRegister.find_by_email(
                email=provider_schema_object[0][0])
            auth_object.delete_regtration(user_obj.id)

    # assert str(e.value) == "409 Conflict: Users Already Register"

    # Test Cases For Provider Register End

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
    #         authdata_object.email = "yogendra@gmail.com"
    #         authdata_object.password = "12345"
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
