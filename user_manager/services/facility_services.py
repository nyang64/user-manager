import logging
from collections import namedtuple

from db import db
from model.address import Address
from model.facilities import Facilities
from model.providers import Providers
from model.patients_providers import PatientsProviders
from model.provider_role_types import ProviderRoleTypes
from model.providers_roles import ProviderRoles
from services.repository.db_repositories import DbRepository
from utils.constants import STUDY_COORDINATOR, OUTPATIENT_PROVIDER, PRESCRIBING_PROVIDER

from sqlalchemy import exc
from werkzeug.exceptions import InternalServerError


class FacilityService(DbRepository):
    def __init__(self):
        pass

    def register_facility(
        self, address, facility_name, on_call_phone, external_facility_id
    ):
        """ Commit the transcation"""
        logging.info("Transcation Started.")
        try:
            if address:
                address_id = self.save_address(address)
            else:
                address_id = None
            facility_id = self.save_facility(
                facility_name, address_id, on_call_phone, external_facility_id
            )
            self.commit_db()
            logging.info("Transcation Completed")
            return address_id, facility_id
        except exc.SQLAlchemyError as error:
            raise InternalServerError(str(error))

    def check_facility_exists_by_external_id(self, external_facility_id) -> bool:
        """Check for existing facility in facilities table"""
        logging.info("Checking for existing facility")
        try:
            facility = Facilities.find_by_external_id(_ext_id=external_facility_id)
            if facility:
                logging.info("Facility {} already exists".format(facility))
                return True
            return False
        except exc.SQLAlchemyError as error:
            logging.error("Error Occured {}".format(str(error)))
            raise InternalServerError(str(error))

    def get_facility_by_id(self, facility_id):
        logging.info("Get facility by id")
        try:
            facility = Facilities.find_by_id(_id=facility_id)
            return facility
        except Exception as e:
            raise InternalServerError(str(e))

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
                        facility_address.postal_code,
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
        """Flush the address transcation"""
        logging.info("Binding Address Data")
        try:
            self.flush_db(address)
            logging.info("Flushed the Address data")
            if address.id is None:
                logging.error("Failed to Save Address")
                raise exc.SQLAlchemyError("Error while adding address")
            return address.id
        except exc.SQLAlchemyError as error:
            logging.error("Error Occured {}".format(str(error)))
            raise InternalServerError(str(error))

    def save_facility(
        self, facility_name, address_id, on_call_phone, external_facility_id
    ):
        """ Flush the Facility transcation"""
        logging.info("Binding Facility Data")
        try:
            facilities = Facilities(
                address_id=address_id,
                name=facility_name,
                on_call_phone=on_call_phone,
                external_facility_id=external_facility_id,
            )
            self.flush_db(facilities)
            logging.info("Flushed the Facility data")
            if facilities.id is None:
                logging.error("Failed to Save Facility")
                raise exc.SQLAlchemyError("Error while adding facility")
            return facilities.id
        except exc.SQLAlchemyError as error:
            logging.error("Error Occured {}".format(str(error)))
            raise InternalServerError(str(error))

    def update_facility(
        self, facility_id, address, facility_name, on_call_phone, external_facility_id
    ):
        logging.info("Updating Facility Data")
        try:
            facility_from_db = Facilities.find_by_id(facility_id)
            if facility_from_db is None:
                logging.error(f"Could not find facility with the ID: {facility_id}")
                raise InternalServerError(
                    f"Could not find facility with the ID: {facility_id}"
                )

            # check if the address needs to be updated
            if address:
                facility_address_from_db = Address.find_by_id(
                    facility_from_db.address_id
                )

                # If address does not exist, create new address, otherwise update address
                if facility_address_from_db:
                    self.__update_address(facility_address_from_db, address)
                else:
                    self.save_address(address)

            self.__update_facility_data(
                facility_from_db,
                name=facility_name,
                on_call_phone=on_call_phone,
                external_facility_id=external_facility_id,
                address_id=address.id,
            )

            self.commit_db()
        except Exception as error:
            logging.error("Error Occured {}".format(str(error)))
            raise InternalServerError(str(error))

    def get_filtered_facilities(self, page_number, record_per_page, name, external_id):
        facilities_list = namedtuple(
            "FacilitiesList",
            (
                "name",
                "external_id",
                "address",
                "phone",
                "num_of_patients",
                "study_coordinator",
                "facility_id",
            ),
        )

        # Get all facilities and address
        facilities_query = db.session.query(Facilities)
        facilities_query = facilities_query.join(
            Address, Facilities.address_id == Address.id
        )

        facilities_query = facilities_query.with_entities(
            Facilities.external_facility_id,
            Facilities.name,
            Facilities.on_call_phone,
            Address.street_address_1,
            Address.city,
            Address.state,
            Address.postal_code,
            Facilities.id,
        )

        if external_id is not None and len(external_id) > 0:
            facilities_query = facilities_query.filter(
                Facilities.external_facility_id == external_id
            )

        if name is not None and len(name) > 0:
            facilities_query = facilities_query.filter(Facilities.name.ilike(name))

        data_count = facilities_query.count()
        query_data = []
        lists = []
        try:
            query_data = (
                facilities_query.order_by(Facilities.name)
                .paginate(page_number + 1, record_per_page)
                .items
            )
        except Exception as e:
            logging.exception(e)

        study_coordinator_role_id = ProviderRoleTypes.find_by_name(
            _name=STUDY_COORDINATOR
        ).id
        outpatient_role_id = ProviderRoleTypes.find_by_name(
            _name=OUTPATIENT_PROVIDER
        ).id

        for data in query_data:
            # Get the study coordinator name

            (
                study_coordinators,
                patients_count,
            ) = self.__find_study_coordinator_and_patients_count(
                data[7], study_coordinator_role_id, outpatient_role_id
            )

            study_coordinator_name = ""
            if len(study_coordinators) > 0:
                study_coordinator_name = study_coordinators[0]

            facilities = facilities_list(
                external_id=data[0],
                name=data[1],
                phone=data[2],
                address=data[3] + " " + data[4] + ", " + data[5] + " " + data[6],
                facility_id=data[7],
                num_of_patients=patients_count,
                study_coordinator=study_coordinator_name,
            )

            lists.append(facilities._asdict())

        return lists, data_count

    def get_all_facilities_providers(self):
        """
        Return a list of all facilities with all types of providers
        """
        facilities = Facilities.all()
        if facilities is None or len(facilities) == 0:
            return None

        data_list = []
        for facility in facilities:
            study_coordinator, outpatient_providers, prescribing_providers = \
                    self.__get_all_providers_for_site(facility.id)
            data = self.__build_facilities_provider_obj(facility, study_coordinator,
                                                        outpatient_providers, prescribing_providers)
            data_list.append(data)

        return data_list


    def __update_address(self, address_from_db, new_address):
        address_from_db.street_address_1 = new_address.street_address_1
        address_from_db.street_address_2 = new_address.street_address_2
        address_from_db.city = new_address.city
        address_from_db.state = new_address.state
        address_from_db.country = new_address.country
        address_from_db.postal_code = new_address.postal_code

        self.flush_db(address_from_db)

    def __update_facility_data(
        self,
        facility_from_db,
        name,
        on_call_phone,
        external_facility_id,
        address_id=None,
    ):
        facility_from_db.name = name
        facility_from_db.on_call_phone = on_call_phone
        facility_from_db.external_facility_id = external_facility_id
        if address_id:
            facility_from_db.address_id = address_id

        self.flush_db(facility_from_db)

    def __find_study_coordinator_and_patients_count(
        self, facility_id, study_coordinator_role_id, outpatient_role_id
    ):
        providers = Providers.find_by_facility_id(facility_id)

        study_coordinators = []
        patients_count = 0

        if providers is not None and len(providers) > 0:
            for provider in providers:
                patients = PatientsProviders.find_patients_by_provider_and_role_id(
                    provider.id, outpatient_role_id
                )
                patients_count += len(patients)

                provider_role = ProviderRoles.find_by_provider_id(
                    _provider_id=provider.id
                )
                if study_coordinator_role_id == provider_role[0].provider_role_id:
                    study_coordinators.append(
                        provider.user.first_name + " " + provider.user.last_name
                    )

        return study_coordinators, patients_count


    def __get_all_providers_for_site(self, facility_id):
        study_coordinator_role_id = \
            ProviderRoleTypes.find_by_name(_name=STUDY_COORDINATOR).id
        outpatient_role_id = \
            ProviderRoleTypes.find_by_name(_name=OUTPATIENT_PROVIDER).id
        prescribing_role_id = \
            ProviderRoleTypes.find_by_name(_name=PRESCRIBING_PROVIDER).id

        # Assumption at this point is that there is going to be only one site investigator (Outpatient provider)
        providers = Providers.find_by_facility_id(facility_id)

        study_coordinator = []
        outpatient_provider = []
        prescribing_provider = []

        if providers is not None and len(providers) > 0:
            for provider in providers:
                provider_role = ProviderRoles.find_by_provider_id(
                    _provider_id=provider.id
                )
                if study_coordinator_role_id == provider_role[0].provider_role_id:
                    study_coordinator_name = provider.user.first_name + " " + provider.user.last_name
                    study_coordinator.append(provider)

                if outpatient_role_id ==  provider_role[0].provider_role_id:
                    outpatient_provider.append(provider)

                if prescribing_role_id == provider_role[0].provider_role_id:
                    prescribing_provider.append(provider)

        return study_coordinator, outpatient_provider, prescribing_provider


    def __build_facilities_provider_obj(self, facility, study_coordinator,
                                        outpatient_providers, prescribing_providers):
        providers = []
        for provider in prescribing_providers:
            prov_json = {
                "name": provider.user.first_name + " " + provider.user.last_name,
                "id": provider.id,
                "email": provider.user.registration.email,
                "phone": provider.user.phone_number
            }
            providers.append(prov_json)

        pi_data = {}
        if len(outpatient_providers) > 0:
            pi_data = {
                "name": outpatient_providers[0].user.first_name + " " + outpatient_providers[0].user.last_name,
                "id": outpatient_providers[0].id
            }

        sc_data = ""
        if len(study_coordinator) > 0:
            sc_data = study_coordinator[0].user.first_name + " " + study_coordinator[0].user.last_name

        data = {
            "site_name" : facility.name,
            "site_id": facility.id,
            "external_id": facility.external_facility_id,
            "principal_investigator": pi_data,
            "study_coordinator": sc_data,
            "prescribing_providers": providers
        }
        return data

