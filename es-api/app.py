from db import db
from ma import ma
from flask_migrate import Migrate
from config import get_connection_url
from authentication.blueprint import AuthenticationBlueprint
from user.blueprint import UserBluePrint
from patient.blueprint import PatientBluePrint
from provider.blueprint import ProviderBlueprint
from admin.blueprint import AdminBlueprint
from application import Appplication
from device.blueprint import DeviceBlueprint

app = Appplication(__name__, '/v1')
app.config["SQLALCHEMY_DATABASE_URI"] = get_connection_url()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["E_EXCEPTIONS"] = True

migrate = Migrate()
db.init_app(app)
ma.init_app(app)
migrate.init_app(app, db)

auth_blueprint = AuthenticationBlueprint()
app.register_blueprint(auth_blueprint)

user_blueprint = UserBluePrint()
app.register_blueprint(user_blueprint)

provider_blueprint = ProviderBlueprint()
app.register_blueprint(provider_blueprint)

admin_blueprint = AdminBlueprint()
app.register_blueprint(admin_blueprint)

patient_blueprint = PatientBluePrint()
app.register_blueprint(patient_blueprint)

device_blueprint = DeviceBlueprint()
app.register_blueprint(device_blueprint)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000, debug=True)
