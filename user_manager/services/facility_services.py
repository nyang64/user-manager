from werkzeug.exceptions import InternalServerError
from services.repository.db_repositories import DbRepository
from model.facilities import Facilities
from model.address import Address
from sqlalchemy import exc


class FacilityService(DbRepository):
    def __init__(self):
        pass

    def register_facility(self, address, facility_name):
        ''' Commit the transcation'''
        try:
            address_id = self.save_address(address)
            facility_id = self.save_facility(facility_name, address_id)
            self.commit_db()
            return address_id, facility_id
        except exc.SQLAlchemyError as error:
            raise InternalServerError(str(error))

    def save_address(self, address):
        '''Flush the address transcation'''
        try:
            addr = Address(street_address_1=address.get('street_address_1'),
                           street_address_2=address.get('street_address_2'),
                           full_address=address.get('full_address'),
                           city=address.get('city'),
                           state=address.get('state'),
                           country=address.get('country'),
                           postal_code=address.get('postal_code'))
            self.flush_db(addr)
            if addr.id is None:
                raise exc.SQLAlchemyError('Error while adding address')
            return addr.id
        except exc.SQLAlchemyError as error:
            raise InternalServerError(str(error))

    def save_facility(self, facility_name, address_id):
        ''' Flush the Facility transcation'''
        try:
            facilities = Facilities(address_id=address_id,
                                    name=facility_name)
            self.flush_db(facilities)
            if facilities.id is None:
                raise exc.SQLAlchemyError('Error while adding facility')
            return facilities.id
        except exc.SQLAlchemyError as error:
            raise InternalServerError(str(error))
