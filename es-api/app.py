from flask import Flask, Blueprint
from flask_restful import Api
from db import db
from ma import ma
from database.dbconnection import getConString
from resources.user.user import (
    UserLogin, UserRegister, UpdateUserPassword, refreshAccessToken,
    ResetUserPassword
)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getConString()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
main_bp = Blueprint('api', __name__)
api = Api(main_bp)
app.register_blueprint(main_bp)

'''
@app.before_first_request
def create_tables():
    db.create_all()
'''
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(UpdateUserPassword, "/updatepassword")
api.add_resource(refreshAccessToken, "/refresh")
api.add_resource(ResetUserPassword, "/resetpassword")
if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)

    app.run(port=5000, debug=True)
