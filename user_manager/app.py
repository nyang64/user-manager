from db import db
from ma import ma
from flask_migrate import Migrate
from flask_seeder import FlaskSeeder
from flask_cors import CORS
from config import get_connection_url
from blueprint.auth_blueprint import AuthenticationBlueprint
from blueprint.user_blueprint import UserBluePrint
from blueprint.patient_blueprint import PatientBluePrint
from blueprint.provider_blueprint import ProviderBlueprint
from application import Appplication
import logging

app = Appplication(__name__, '/')
app.config["SQLALCHEMY_DATABASE_URI"] = get_connection_url()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["E_EXCEPTIONS"] = True

# enable cors for all endpoints from any location
CORS(app)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

migrate = Migrate()
db.init_app(app)
ma.init_app(app)
migrate.init_app(app, db)

seeder = FlaskSeeder()
seeder.init_app(app, db)

auth_blueprint = AuthenticationBlueprint()
app.register_blueprint(auth_blueprint)

user_blueprint = UserBluePrint()
app.register_blueprint(user_blueprint)

provider_blueprint = ProviderBlueprint()
app.register_blueprint(provider_blueprint)

patient_blueprint = PatientBluePrint()
app.register_blueprint(patient_blueprint)


if __name__ == "__main__":

    # NOTE: DO NOT change the host and port numbers while deploying to cloud. The application
    # WILL NOT work as the port is tied to ECS container. If the port is changed here, we need to
    # make changes to the ECS infrastructure.
    logging.info('App is up')
    app.run(host='0.0.0.0', port=5000, debug=True)
