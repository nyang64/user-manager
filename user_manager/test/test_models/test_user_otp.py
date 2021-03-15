import pytest
from model.user_otp import UserOTPModel
import os
from application import Appplication
from config import get_connection_url
from flask_migrate import Migrate
from db import db
from ma import ma


@pytest.fixture
def set_os_environ():
    os.environ['POSTGRES_DB_PORT'] = "0"

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


class TestClass:
    # def test_user_otp_schema_with_none(self, flask_app, set_os_environ):
    #     with flask_app.app_context():
    #         with pytest.raises(Exception) as e:
    #             assert UserOTPModel.matchOTP('1', '1')
    #         assert "500 Internal Server Error" in str(e.value)
