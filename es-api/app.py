from flask import Flask, Blueprint
from flask_restful import Api
from db import db
from ma import ma
from flask_migrate import Migrate
from database.dbconnection import getConString
from resources.user.user import UserRegister,UserLogin

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getConString()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PROPAGATE_EXCEPTIONS"] = True
main_bp = Blueprint('api', __name__)
api = Api(main_bp)
app.register_blueprint(main_bp)
migrate = Migrate()
db.init_app(app)
ma.init_app(app)
migrate.init_app(app, db)


api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
