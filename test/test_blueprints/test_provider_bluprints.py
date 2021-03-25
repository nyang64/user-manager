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
            yield resp.json


class TestProviderBluePrint:
    ids = []

    # Test Cases For Register_Provider Start
    def test_register_provider_with_valid_data(
            self, flask_app, mocker: MockerFixture):
        with flask_app.app_context():
            with flask_app.test_client() as client:
                test_token = os.environ["test_token"]
                header = Headers(
                    {
                        'Authorization': test_token
                    })
                resp = client.post(
                    '/v1/provider/register',
                    json=dict(
                        first_name="test123",
                        last_name="test12345",
                        facility_id="1",
                        phone_number="998877611",
                        email="provider123@elementsci.com",
                        password="test123"),
                    follow_redirects=True,
                    headers=header)
                assert resp.status_code == 201

    def test_register_provider_with_existing_data(
            self, flask_app, mocker: MockerFixture):
        with flask_app.app_context():
            with flask_app.test_client() as client:
                test_token = os.environ["test_token"]
                header = Headers(
                    {
                        'Authorization': test_token
                    })
                resp = client.post(
                    '/v1/provider/register',
                    json=dict(
                        first_name="test123",
                        last_name="test12345",
                        facility_id="1",
                        phone_number="998877611",
                        email="provider123@elementsci.com",
                        password="test123"),
                    follow_redirects=True,
                    headers=header)
                assert resp.status_code == 409

    def test_register_provider_with_invalid_token(
            self, flask_app):
        with flask_app.app_context():
            with flask_app.test_client() as client:
                test_token = 'test123'
                header = Headers(
                    {
                        'Authorization': test_token
                    })
                resp = client.post(
                    '/v1/provider/register',
                    json=dict(
                        first_name="test123",
                        last_name="test12345",
                        facility_id="1",
                        phone_number="998877611",
                        email="provider123@elementsci.com",
                        password="test123"),
                    follow_redirects=True,
                    headers=header)
                assert resp.status_code == 401

    # Test Cases For Get Provider List Start
    def test_get_provider_list_with_valid_data(
            self, flask_app, mocker: MockerFixture):
        with flask_app.app_context():
            with flask_app.test_client() as client:
                test_token = os.environ["test_token"]
                header = Headers(
                    {
                        'Authorization': test_token
                    })
                resp = client.get(
                    '/v1/providers',
                    follow_redirects=True,
                    headers=header)
                provider_ids = resp.json
                print(resp.json)
                for ids in provider_ids['Data']:
                    print(ids["id"])
                    self.ids.append(ids["id"])
                assert resp.status_code == 200
    # Test Cases For Get Provider List End

    # Test Cases For Get Provider By Id
    def test_get_provider_by_id_with_valid_data(
            self, flask_app, mocker: MockerFixture):
        with flask_app.app_context():
            with flask_app.test_client() as client:
                test_token = os.environ["test_token"]
                header = Headers(
                    {
                        'Authorization': test_token
                    })
                resp = client.get(
                    '/v1/provider/get?provider_id='+str(
                        self.ids[0]),
                    follow_redirects=True,
                    headers=header)
                assert resp.status_code == 200

    # Test Cases For Update Provider
    def test_update_provider_with_valid_data(
            self, flask_app, provider_token):
        with flask_app.app_context():
            with flask_app.test_client() as client:
                test_token = os.environ["test_token"]
                header = Headers(
                    {
                        'Authorization': test_token
                    })
                resp = client.put(
                    '/v1/provider/update',
                    follow_redirects=True,
                    json=dict(
                        provider_id=self.ids[0],
                        first_name="yogendra",
                        last_name="rai",
                        phone_number="88888888"
                    ),
                    headers=header)
                # print(resp.json)
                assert resp.status_code == 200

    # Test Cases For Get Patient List
    def test_patient_list(
            self, flask_app, provider_token):
        with flask_app.app_context():
            with flask_app.test_client() as client:
                test_token = provider_token["id_token"]
                # print(test_token)
                header = Headers(
                    {
                        'Authorization': test_token
                    })
                resp = client.post(
                    '/v1/patients/list',
                    follow_redirects=True,
                    json=dict(
                        page_number="0",
                        record_per_page="20",
                        ),
                    headers=header)
                print(resp.json)
                assert resp.status_code == 200

    def test_get_patient_device_list(self, flask_app, provider_token):
        with flask_app.app_context():
            with flask_app.test_client() as client:
                test_token = provider_token["id_token"]
                # print(test_token)
                header = Headers(
                    {
                        'Authorization': test_token
                    })
                resp = client.get(
                    '/v1/patient/detail?patientID='+str(
                        os.environ["patient_ids"]),
                    follow_redirects=True,
                    headers=header)
                assert resp.status_code == 200

    # Test Cases For Delete_Patient Start
    def test_delete_patient_with_existing_data(
            self, flask_app, mocker: MockerFixture):
        with flask_app.app_context():
            with flask_app.test_client() as client:
                test_token = os.environ["test_token"]
                header = Headers(
                    {
                        'Authorization': test_token
                    })
                resp = client.delete(
                    '/v1/patients?id='+str(os.environ["patient_ids"]),
                    follow_redirects=True,
                    headers=header)
                assert resp.status_code == 200

    # Test Cases For Delete Provider
    def test_delete_provider_with_valid_data(
            self, flask_app, mocker: MockerFixture):
        with flask_app.app_context():
            with flask_app.test_client() as client:
                test_token = os.environ["test_token"]
                header = Headers(
                    {
                        'Authorization': test_token
                    })
                resp = client.delete(
                    '/v1/provider/delete',
                    json=dict(
                        provider_id=self.ids[0]),
                    follow_redirects=True,
                    headers=header)
                assert resp.status_code == 200

    # Test Cases For Add Facility
    def test_add_facility_with_valid_data(
            self, flask_app, mocker: MockerFixture):
        with flask_app.app_context():
            with flask_app.test_client() as client:
                test_token = os.environ["test_token"]
                header = Headers(
                    {
                        'Auth9orization': test_token
                    })
                resp = client.post(
                    '/v1/add/facility',
                    follow_redirects=True,
                    json=dict(
                        facility_name="Test Facility",
                        address="Test Address"),
                    headers=header)
                assert resp.status_code == 400
