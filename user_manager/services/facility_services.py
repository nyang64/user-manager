import logging

from model.address import Address
from model.facilities import Facilities
from services.repository.db_repositories import DbRepository
from sqlalchemy import exc
from werkzeug.exceptions import InternalServerError


class FacilityService(DbRepository):
    def __init__(self):
        pass

    def register_facility(self, address, facility_name, on_call_phone, external_facility_id):
        ''' Commit the transcation'''
        logging.info('Transcation Started.')
        try:
            if address:
                address_id = self.save_address(address)
            else:
                address_id = None
            facility_id = self.save_facility(facility_name, address_id, on_call_phone, external_facility_id)
            self.commit_db()
            logging.info('Transcation Completed')
            return address_id, facility_id
        except exc.SQLAlchemyError as error:
            raise InternalServerError(str(error))

    def check_facility_exists(self, external_facility_id) -> bool:
        '''Check for existing facility in facilities table'''
        logging.info("Checking for existing facility")
        try:
            facility = Facilities.find_by_external_id(_ext_id=external_facility_id)
            if facility:
                logging.info("Facility {} already exists".format(facility))
                return True
            return False
        except exc.SQLAlchemyError as error:
            logging.error('Error Occured {}'.format(str(error)))
            raise InternalServerError(str(error)) 

    def list_all_facilities(self):
        """List all facility records"""
        logging.info("List all facilities")
        try:
            facilities = Facilities.all()
            data_count = len(facilities)
            f_list = []

            for facility in facilities:
                address = ""
                if facility.address_id:
                    facility_address = Address.find_by_id(facility.address_id)
                    address = "{} {}, {}, {} {} {}".format(
                        facility_address.street_address_1,
                        facility_address.street_address_2,
                        facility_address.city,
                        facility_address.state,
                        facility_address.country,
                        facility_address.postal_code
                    )
                facilites_dict = {}
                facilites_dict["name"] = facility.name
                facilites_dict["on_call_phone"] = facility.on_call_phone
                facilites_dict["external_facility_id"] = facility.external_facility_id
                facilites_dict["id"] = facility.id
                facilites_dict["address"] = address
                f_list.append(facilites_dict)

            return f_list, data_count
        except exc.SQLAlchemyError as error:
            logging.error("Error occured: {}".format(str(error)))
            raise InternalServerError(str(error))

    def save_address(self, address):
        '''Flush the address transcation'''
        logging.info('Binding Address Data')
        try:
            self.flush_db(address)
            logging.info('Flushed the Address data')
            if address.id is None:
                logging.error('Failed to Save Address')
                raise exc.SQLAlchemyError('Error while adding address')
            return address.id
        except exc.SQLAlchemyError as error:
            logging.error('Error Occured {}'.format(str(error)))
            raise InternalServerError(str(error))

    def save_facility(self, facility_name, address_id, on_call_phone, external_facility_id):
        ''' Flush the Facility transcation'''
        logging.info('Binding Facility Data')
        try:
            facilities = Facilities(address_id=address_id,
                                    name=facility_name,
                                    on_call_phone=on_call_phone,
                                    external_facility_id=external_facility_id)
            self.flush_db(facilities)
            logging.info('Flushed the Facility data')
            if facilities.id is None:
                logging.error('Failed to Save Facility')
                raise exc.SQLAlchemyError('Error while adding facility')
            return facilities.id
        except exc.SQLAlchemyError as error:
            logging.error('Error Occured {}'.format(str(error)))
            raise InternalServerError(str(error))
