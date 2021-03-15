import pytest
from model.user_registration import UserRegister
from application import Appplication
from config import get_connection_url
from flask_migrate import Migrate
from db import db
from ma import ma

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
    def test_base_schema_with_not_found(self, flask_app):
        with flask_app.app_context():
            UserRegister.delete_user_by_Userid(200000)
