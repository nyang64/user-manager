from application import Appplication


def create_test_app():
    ''' Mock the flask app and register all the endpoint'''
    from db import db
    from ma import ma
    app = Appplication(__name__, '/v1')
    db.init_app(app)
    ma.init_app(app)

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config["E_EXCEPTIONS"] = True
    app.config["TESTING"] = True
    return app
