from flask import Flask, Blueprint
from flask_restful import Api
from db import db
from ma import ma
from flask_migrate import Migrate
from database.dbconnection import getConString
from resources.user.user import (
    UserLogin, UserRegister, UpdateUserPassword, refreshAccessToken,
    ResetUserPassword
)
from user.blueprint import UserBluePrint

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getConString()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PROPAGATE_EXCEPTIONS"] = True
main_bp = Blueprint('api', __name__)
api = Api(main_bp)
app.register_blueprint(main_bp)

'''
@app.before_first_request
def create_tables():
    db.create_all()
'''
migrate = Migrate()
db.init_app(app)
ma.init_app(app)
migrate.init_app(app, db)


# api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/auth/token")
api.add_resource(UpdateUserPassword, "/updatepassword")
api.add_resource(refreshAccessToken, "/refresh")
api.add_resource(ResetUserPassword, "/resetpassword")

user_blueprint = UserBluePrint()
app.register_blueprint(user_blueprint)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
