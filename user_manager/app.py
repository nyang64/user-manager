import os
from db import db
from ma import ma
from flask_migrate import Migrate
from flask_seeder import FlaskSeeder
from config import get_connection_url
from blueprint.auth_blueprint import AuthenticationBlueprint
from blueprint.user_blueprint import UserBluePrint
from blueprint.patient_blueprint import PatientBluePrint
from blueprint.provider_blueprint import ProviderBlueprint
from application import Appplication
import pdb

app = Appplication(__name__, '/v1')
app.config["SQLALCHEMY_DATABASE_URI"] = get_connection_url()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["E_EXCEPTIONS"] = True
app.debug = True

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
    app.run(
        host=os.environ.get("APP_HOST"),
        port=os.environ.get("APP_PORT"),
        debug=os.environ.get("APP_DEBUG"),
    )
