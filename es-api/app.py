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

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getConString()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PROPAGATE_EXCEPTIONS"] = True
main_bp = Blueprint('api', __name__)
api = Api(main_bp)
app.register_blueprint(main_bp)
<<<<<<< HEAD

'''
@app.before_first_request
def create_tables():
    db.create_all()
'''
=======
migrate = Migrate()
db.init_app(app)
ma.init_app(app)
migrate.init_app(app, db)


>>>>>>> 065d703665fe9c5be8ffdc9cb68403dc7077e3c6
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(UpdateUserPassword, "/updatepassword")
api.add_resource(refreshAccessToken, "/refresh")
api.add_resource(ResetUserPassword, "/resetpassword")
if __name__ == "__main__":
    app.run(port=5000, debug=True)
