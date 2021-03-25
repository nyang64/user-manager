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


@pytest.fixture
def provider_token(flask_app):
    with flask_app.app_context():
        with flask_app.test_client() as client:
            resp = client.post('/v1/auth/token', json=dict(
                email="provider123@elementsci.com",
                password="test123"
            ), follow_redirects=True)
            print(resp.json)
            yield resp.json


class TestPatientBluePrint:
    ids = []

    # Test Cases For Register_Patient Start
    def test_register_patient_with_valid_data(
            self, flask_app, mocker: MockerFixture):
        with flask_app.app_context():
            with flask_app.test_client() as client:
                test_token = os.environ["test_token"]
                header = Headers(
                    {
                        'Authorization': test_token
                    })
                resp = client.post(
                    '/v1/patients',
                    json=dict(
                        email="test_12345@gmail.com",
                        password="test12345",
                        first_name="dhr",
                        last_name="rana",
                        phone_number="8097865432",
                        emergency_contact_name="test",
                        emergency_contact_number="1212121212",
                        date_of_birth="2019-08-08",
                        gender="Male"
                    ),
                    follow_redirects=True,
                    headers=header)
                print(resp.json)
                self.ids.append(resp.json["data"]["patient_id"])
                os.environ["patient_ids"] = str(
                    resp.json["data"]["patient_id"])
                assert resp.status_code == 201

    def test_register_patient_with_existing_data(
            self, flask_app, mocker: MockerFixture):
        with flask_app.app_context():
            with flask_app.test_client() as client:
                test_token = os.environ["test_token"]
                header = Headers(
                    {
                        'Authorization': test_token
                    })
                resp = client.post(
                    '/v1/patients',
                    json=dict(
                        email="test_12345@gmail.com",
                        password="test12345",
                        first_name="dhr",
                        last_name="rana",
                        phone_number="8097865432",
                        emergency_contact_name="test",
                        emergency_contact_number="1212121212",
                        date_of_birth="2019-08-08",
                        gender="Male"
                    ),
                    follow_redirects=True,
                    headers=header)
                assert resp.status_code == 409

    # Test Cases For update_Patient Start
    def test_update_patient_with_existing_data(
            self, flask_app, mocker: MockerFixture):
        with flask_app.app_context():
            with flask_app.test_client() as client:
                test_token = os.environ["test_token"]
                header = Headers(
                    {
                        'Authorization': test_token
                    })
                resp = client.put(
                    '/v1/patients?id='+str(os.environ["patient_ids"]),
                    json=dict(
                        emergency_contact_name="yogendra",
                        emergency_contact_number="1212121212",
                        date_of_birth="2019-08-08"
                        ),
                    follow_redirects=True,
                    headers=header)
                assert resp.status_code == 200

    # Test Cases For get_Patient_device_list Start
    def test_get_Patient_device_list(
            self, flask_app, mocker: MockerFixture):
        with flask_app.app_context():
            with flask_app.test_client() as client:
                test_token = os.environ["test_token"]
                header = Headers(
                    {
                        'Authorization': test_token
                    })
                resp = client.get(
                    '/v1/patient/device/get',
                    follow_redirects=True,
                    headers=header)
                assert resp.status_code == 200
