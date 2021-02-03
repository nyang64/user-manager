from model.facilities import Facilities
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import InternalServerError, NotFound
from db import db


class FacilitiesRepository():
    def save_facility(self, address_id, name):
        try:
            facility_data = Facilities(address_id=address_id, name=name)
            facility_data.save_to_db()
            return facility_data.id
        except SQLAlchemyError as error:
            db.session.rollback()
            raise InternalServerError(str(error))