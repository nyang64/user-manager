import os

from application import Appplication
from blueprint.auth_blueprint import AuthenticationBlueprint
from blueprint.patient_blueprint import PatientBluePrint
from blueprint.provider_blueprint import ProviderBlueprint
from blueprint.user_blueprint import UserBluePrint

def get_connection_url():
    """ Get the db connection url"""
    host = os.environ.get("TEST_POSTGRES_DB_HOST")
    port = str(os.environ.get("TEST_POSTGRES_DB_PORT"))
    database_name = os.environ.get("TEST_POSTGRES_DB_NAME")
    user = os.environ.get("TEST_POSTGRES_DB_USER_KEY")
    password = os.environ.get("TEST_POSTGRES_DB_PASSWORD_KEY")
    print(f"postgresql://{user}:{password}@{host}:{port}/{database_name}")
    if (
        host is None
        or port is None
        or database_name is None
        or user is None
        or password is None
    ):
        raise Exception("Database connection error")
    return f"postgresql://{user}:{password}@{host}:{port}/{database_name}"


def create_test_app():
    """ Mock the flask app and register all the endpoint"""
    from db import db
    from ma import ma

    app = Appplication(__name__, "/v1")
    db.init_app(app)
    ma.init_app(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = get_connection_url()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config["E_EXCEPTIONS"] = True
    app.config["TESTING"] = True

    auth_blueprint = AuthenticationBlueprint()
    app.register_blueprint(auth_blueprint)

    user_blueprint = UserBluePrint()
    app.register_blueprint(user_blueprint)

    provider_blueprint = ProviderBlueprint()
    app.register_blueprint(provider_blueprint)

    patient_blueprint = PatientBluePrint()
    app.register_blueprint(patient_blueprint)
    return app
