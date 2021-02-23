from werkzeug.exceptions import InternalServerError
from sqlalchemy import exc
from model.base_model import BaseModel
from db import db


class DbRepository:
    def __init__(self):
        pass

    def save_db(self, obj):
        if not isinstance(obj, BaseModel) and type(BaseModel) == BaseModel:
            raise InternalServerError('Not a valid model')
        try:
            db.session.add(obj)
            db.session.commit()
        except exc.SQLAlchemyError as error:
            db.session.rollback()
            raise InternalServerError(str(error))

    def flush_db(self, obj):
        if not isinstance(obj, BaseModel) and type(BaseModel) == BaseModel:
            raise InternalServerError('Not a valid model')
        try:
            db.session.add(obj)
            db.session.flush()
        except exc.SQLAlchemyError as error:
            raise InternalServerError(str(error))

    def commit_db(self):
        """ if not isinstance(self, BaseModel) and type(BaseModel) == BaseModel:
            raise InternalServerError('Not a valid model') """
        try:
            db.session.commit()
        except exc.SQLAlchemyError as error:
            db.session.rollback()
            raise InternalServerError(str(error))

    def update_db(self, obj):
        if not isinstance(obj, BaseModel) and type(BaseModel) == BaseModel:
            raise InternalServerError('Not a valid model')
        try:
            db.session.commit()
        except exc.SQLAlchemyError as error:
            db.session.rollback()
            raise InternalServerError(str(error))

    def delete_obj(self, obj):
        if not isinstance(obj, BaseModel) and type(BaseModel) == BaseModel:
            raise InternalServerError('Not a valid model')
        try:
            db.session.delete(obj)
            db.session.commit()
        except exc.SQLAlchemyError as error:
            db.session.rollback()
            raise InternalServerError(str(error))
