import logging
import os

from application import Appplication
from blueprint.auth_blueprint import AuthenticationBlueprint
from blueprint.device_blueprint import DeviceBlueprint
from blueprint.patient_blueprint import PatientBluePrint
from blueprint.provider_blueprint import ProviderBlueprint
from blueprint.user_blueprint import UserBluePrint
from config import get_connection_url, read_environ_value
from db import db
from flask_cors import CORS
from flask_migrate import Migrate
from flask_seeder import FlaskSeeder
from ma import ma
from model.patches import Patches
from utils.constants import FLASK_ENV

# Keep "model.patches" (above) until the model is implemented so it gets picked up by Alembic.
# Otherwise, Alembic will try to create a migration to delete the table.

# QA and Development environments run with "FLASK_ENV = production"
# If we need to make calls to QA or Development environments locally,
# update the your environment variable for FLASK_ENV.
# load environment variables when building locally.
print(FLASK_ENV)

if FLASK_ENV != "production" and FLASK_ENV != "test":
    from dotenv import load_dotenv

    load_dotenv(f".env.{FLASK_ENV}")

app = Appplication(__name__, "/")
print(os.getenv("SQLALCHEMY_DATABASE_URI"))
app.config["SQLALCHEMY_DATABASE_URI"] = get_connection_url()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["E_EXCEPTIONS"] = True

# enable cors for all endpoints from any location
CORS(app)
logger = logging.getLogger()
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
print("Log level {}".format(LOG_LEVEL))
logger.setLevel(level=LOG_LEVEL)

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

device_blueprint = DeviceBlueprint()
app.register_blueprint(device_blueprint)


if __name__ == "__main__":

    # NOTE: DO NOT change the host and port numbers while deploying to cloud. The application
    # WILL NOT work as the port is tied to ECS container. If the port is changed here, we need to
    # make changes to the ECS infrastructure.
    logging.info("App is up")
    value = os.environ.get("SECRET_MANAGER_ARN")
    app.run(host="0.0.0.0", port=5000, debug=read_environ_value(value, "DEBUG"))
