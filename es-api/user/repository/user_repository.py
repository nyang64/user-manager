from model.users import Users
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import InternalServerError, NotFound
from db import db


class UserRepository():
    def save_user(self, first_name, last_name, phone_number, email, reg_id):
        try:
            user_data = Users(first_name=first_name,
                              last_name=last_name,
                              phone_number=phone_number,
                              email=email,
                              registration_id=reg_id)
            print('create_user')
            Users.save_user(user_data)
            print('user created')
            return user_data.id
        except SQLAlchemyError as error:
            db.session.rollback()
            raise InternalServerError(str(error))
    
    def update_user_byid(self, id, first_name, last_name, phone_number, email):
        try:
            user_data = db.session.query(Users).filter_by(id=id).first()
            if user_data is None:
                raise NotFound("user doesn't exist")
            print(user_data)
            print('update_user')
            user_data.first_name=first_name
            user_data.last_name=last_name
            user_data.phone_number=phone_number
            user_data.email=email
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            raise InternalServerError(error)
        
    def list_users(self):
        try:
            users_list = db.session.query(Users).all()
            print(users_list)
            print('update_user')
            #Users.save_user(user_data)
            print('user created')
            users_data = [{'id': user.id, 
                           'first_name':user.first_name, 
                           'last_name':user.last_name}
                          for user in users_list]
            return users_data
        except SQLAlchemyError as error:
            db.session.rollback()
            raise InternalServerError(error)
        
    def delete_user_byid(self, id):
        try:
            user = db.session.query(Users).filter_by(id=id).first()
            print(user)
            if user is None:
                raise NotFound('user does not exist')
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            raise InternalServerError(error)