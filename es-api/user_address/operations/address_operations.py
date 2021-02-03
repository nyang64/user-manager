from model.address import Address
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import InternalServerError, NotFound
from db import db


class AddressRepository():
    def save_address(
            self, user_id, street_address_1,
            street_address_2, city, state, country, postal_code):
        try:
            address_data = Address(
                user_id=user_id,
                street_address_1=street_address_1,
                street_address_2=street_address_2,
                city=city,
                state=state,
                country=country,
                postal_code=postal_code
                )
            address_data.save_to_db()
            return address_data.id
        except SQLAlchemyError as error:
            db.session.rollback()
            raise InternalServerError(str(error))