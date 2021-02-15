from db import db
from sqlalchemy import exc
from werkzeug.exceptions import InternalServerError


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column('id', db.Integer, primary_key=True)
    created_at = db.Column('created_at',
                           db.DateTime,
                           default=db.func.now(),
                           nullable=False)
    updated_on = db.Column('updated_at', db.DateTime,
                           default=db.func.now(),
                           onupdate=db.func.now())

    def save_db(self):
        if not isinstance(self, BaseModel) and type(BaseModel) == BaseModel:
            raise InternalServerError('Not a valid model')
        try:
            db.session.add(self)
            db.session.commit()
        except exc.SQLAlchemyError as error:
            db.session.rollback()
            raise InternalServerError(str(error))
        
    def flush_db(self):
        if not isinstance(self, BaseModel) and type(BaseModel) == BaseModel:
            raise InternalServerError('Not a valid model')
        try:
            db.session.add(self)
            db.session.flush()
        except exc.SQLAlchemyError as error:
            raise InternalServerError(str(error))

    def commit_db(self):
        if not isinstance(self, BaseModel) and type(BaseModel) == BaseModel:
            raise InternalServerError('Not a valid model')
        try:
            db.session.commit()
        except exc.SQLAlchemyError as error:
            db.session.rollback()
            raise InternalServerError(str(error))

    def update_db(self):
        if not isinstance(self, BaseModel) and type(BaseModel) == BaseModel:
            raise InternalServerError('Not a valid model')
        try:
            db.session.commit()
        except exc.SQLAlchemyError as error:
            db.session.rollback()
            raise InternalServerError(str(error))

    def delete_obj(self):
        if not isinstance(self, BaseModel) and type(BaseModel) == BaseModel:
            raise InternalServerError('Not a valid model')
        try:
            db.session.delete(self)
            db.session.commit()
        except exc.SQLAlchemyError as error:
            db.session.rollback()
            raise InternalServerError(str(error))
