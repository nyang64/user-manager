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


class TestClass:
    # Test Cases For Provider Register Start

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

    def test_patient_detail_with_valid_data(
                self,
                flask_app,
                provider_object,
                provider_schema_object):
        with flask_app.app_context():
            response = provider_object.patient_detail_byid(
                None
                )
            assert response == ({}, [])

    def test_report_signed_link_valid_data(
                self,
                flask_app,
                provider_object,
                provider_schema_object):
        with flask_app.app_context():
            response = provider_object.report_signed_link(
                None
                )
            assert response == ('No report found', 404)
