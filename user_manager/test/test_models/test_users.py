import pytest
from model.users import Users
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


class TestUsersModel:
    def test_user_get_by_id_none(self, flask_app):
        with flask_app.app_context():
            with pytest.raises(Exception) as e:
                assert Users.getUserById(None)
            assert "500 Internal Server Error" in str(e.value)

    def test_user_get_by_id(self, flask_app):
        with flask_app.app_context():
            Users.getUserById(1)

    def test_user_find_by_email(self, flask_app):
        with flask_app.app_context():
            with pytest.raises(Exception) as e:
                Users.find_by_email(None)
            assert "has no property" in str(e.value)
