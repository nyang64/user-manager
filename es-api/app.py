from db import db
from ma import ma
from flask_migrate import Migrate
from config import get_connection_url
from authentication.blueprint import AuthenticationBlueprint
from user.blueprint import UserBluePrint
from patient.blueprint import PatientBluePrint
from provider.blueprint import ProviderBlueprint
from application import Appplication
from utils.init_db import initializeDB

app = Appplication(__name__, '/v1')
app.config["SQLALCHEMY_DATABASE_URI"] = get_connection_url()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PROPAGATE_EXCEPTIONS"] = True

migrate = Migrate()
db.init_app(app)
ma.init_app(app)
migrate.init_app(app, db)


@app.before_first_request
def create_tables():
    db.create_all()
    initDB = initializeDB()




auth_blueprint = AuthenticationBlueprint()
app.register_blueprint(auth_blueprint)

user_blueprint = UserBluePrint()
app.register_blueprint(user_blueprint)

provider_blueprint = ProviderBlueprint()
app.register_blueprint(provider_blueprint)

patient_blueprint = PatientBluePrint()
app.register_blueprint(patient_blueprint)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
