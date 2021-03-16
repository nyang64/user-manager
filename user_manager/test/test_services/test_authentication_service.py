from application import Appplication
from ma import ma
from config import get_connection_url
import pytest
from db import db
from flask_migrate import Migrate
from services.auth_services import AuthServices
from model.user_registration import UserRegister
from model.user_otp import UserOTPModel
from utils.common import have_keys


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


@pytest.fixture
def auth_object():
    authObject = AuthServices()
    yield authObject


@pytest.fixture
def authdata_object():
    authData = UserRegister()
    yield authData


@pytest.fixture
def otp_not_exist_object():
    otp_mdl = UserOTPModel()
    otp_mdl.user_id = None
    otp_mdl.otp = None
    otp_mdl.temp_password = None
    yield otp_mdl


@pytest.fixture
def otp_existing_object():
    otp_mdl = UserOTPModel()
    otp_mdl.user_id = 1
    otp_mdl.otp = 11111111
    otp_mdl.temp_password = 12345678
    yield otp_mdl


class TestClass:
    # Test Cases For User_login Start

    def test_User_login_with_unregisterd_user(
            self, flask_app, auth_object, authdata_object):
        with flask_app.app_context():
            authdata_object.email = "yogendra_2667@gmail.com"
            authdata_object.password = "12345"
            with pytest.raises(Exception) as e:
                assert auth_object.User_login(authdata_object)
            assert str(e.value) == "404 Not Found: No Such User Exist"

    def test_User_login_with_invalid_credentials(
            self, flask_app, auth_object, authdata_object):
        with flask_app.app_context():
            authdata_object.email = "yogendra.rai@infostretch.com"
            authdata_object.password = "1234511"
            with pytest.raises(Exception) as e:
                assert auth_object.User_login(authdata_object)
            assert str(e.value) == "401 Unauthorized: Invalid Credentials"

    def test_User_login_with_valid_credentials(
            self, flask_app, auth_object, authdata_object):
        with flask_app.app_context():
            authdata_object.email = "yogendra.rai@infostretch.com"
            authdata_object.password = "12345"
            response_obj = auth_object.User_login(authdata_object)
            assert type(response_obj) is dict
            assert have_keys(
                response_obj,
                'id_token',
                'first_name',
                'last_name',
                'user_status',
                'isFirstTimeLogin',
                'message',
                'refresh_token') is True

    def test_User_login_with_no_data(
            self, flask_app, auth_object, authdata_object):
        with flask_app.app_context():
            with pytest.raises(Exception) as e:
                assert auth_object.User_login(authdata_object)
            assert str(e.value) == "404 Not Found: No Such User Exist"

    # Test Cases For User_login End

    # Test Cases For Refresh_token Start
    def test_refresh_token(self, flask_app, auth_object, authdata_object):
        with flask_app.app_context():
            response_obj = auth_object.refresh_user_token(
                'yogendra.rai@gmail.com')
            assert type(response_obj) is dict
            assert have_keys(
                response_obj,
                'id_token',
                'isFirstTimeLogin',
                'message',
                'refresh_token') is True

    # Test Cases For Refresh_token Start

    # Test Cases For update Password Start

    def test_update_password_unregisted_user(self, flask_app, auth_object):
        with flask_app.app_context():
            with pytest.raises(Exception) as e:
                assert auth_object.update_password(
                    'yogendra.rai@gmail.com',
                    '12345')
                assert str(e.value) == "404 Not Found: No Such User Exist"

    def test_update_password_registed_user(self, flask_app, auth_object):
        with flask_app.app_context():
            with pytest.raises(Exception) as e:
                auth_obj = auth_object.update_password(
                    'yogendra.rai@infostretch.com',
                    '12345')
                assert (200 in auth_obj) is True
                assert (
                    {'message': 'Password Updated'} in auth_obj
                    ) is True
                if e is not None:
                    # To handel Database Max Pool Exception
                    assert ('500' in str(e.value)) is True
    # Test Cases For update Password End

    # Test Cases For Update OTP Start
    def test_update_otp_unregisted_user(
            self, flask_app, auth_object, otp_not_exist_object):
        with flask_app.app_context():
            auth_object.update_otp_data(
                otp_not_exist_object)
            with pytest.raises(Exception) as e:
                assert auth_object.update_otp_data(
                    otp_not_exist_object)
                assert str(e.value) == "404 Not Found: No Such User Exist"

    def test_update_otp_registed_user(
            self, flask_app, auth_object, otp_existing_object):
        with flask_app.app_context():
            with pytest.raises(Exception) as e:
                assert auth_object.update_otp_data(
                    otp_existing_object)
                assert str(e.value) == "404 Not Found: No Such User Exist"

    # Test Cases For Send OTP END
