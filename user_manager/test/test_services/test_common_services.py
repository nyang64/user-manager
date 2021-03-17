from services.common_services import CommonRepo
from application import Appplication
from ma import ma
from config import get_connection_url
import pytest
from db import db
from flask_migrate import Migrate


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
def commpoRepo():
    comm_repo = CommonRepo()
    yield comm_repo


class TestCommonService:
    def test_check_patient_exist(self, flask_app, commpoRepo):
        with flask_app.app_context():
            with pytest.raises(Exception) as e:
                assert commpoRepo.check_patient_exist(None)
            assert "404 Not Found" in str(e.value)

    def test_is_email_registerd_with_none(self, flask_app, commpoRepo):
        with flask_app.app_context():
            commpoRepo.is_email_registered(None)

    def test_is_email_registerd_with_registerd(self, flask_app, commpoRepo):
        with flask_app.app_context():
            with pytest.raises(Exception) as e:
                assert commpoRepo.is_email_registered('esadmin@elementsci.com')
            assert "409 Conflict" in str(e.value)
