from application import Appplication


def create_test_app():
    ''' Mock the flask app and register all the endpoint'''
    app = Appplication(__name__, '/v1')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config["E_EXCEPTIONS"] = True
    app.config["TESTING"] = True
    return app
