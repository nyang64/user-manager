import logging
from collections import namedtuple

from datetime import datetime
from db import db
from model.address import Address
from model.facilities import Facilities
from model.patient import Patient
from model.patients_providers import PatientsProviders
from model.provider_role_types import ProviderRoleTypes
from model.providers import Providers
from model.salvos import Salvos
from model.therapy_reports import TherapyReport
from model.user_registration import UserRegister
from model.user_status import UserStatus
from model.user_status_type import UserStatusType
from model.users import Users
from schema.providers_roles_schema import ProvidersRolesSchema
from schema.providers_schema import ProvidersSchema
from services.auth_services import AuthServices
from services.repository.db_repositories import DbRepository
from services.user_services import UserServices
from sqlalchemy.exc import SQLAlchemyError
from utils.constants import PROVIDER
from utils.common import generate_random_password, encPass
from utils.send_mail import send_provider_registration_email
from sqlalchemy import exc
from werkzeug.exceptions import InternalServerError, NotFound

provider_role_schema = ProvidersRolesSchema()
provider_schema = ProvidersSchema()


class ProviderService(DbRepository):
    def __init__(self):
        self.auth_obj = AuthServices()
        self.user_obj = UserServices()

    def register_provider_service(self, register, user, facility_id, role, is_primary_provider):
        try:
            # Save data in the registration table
            reg_id = self.auth_obj.register_new_user(register[0], register[1])

            # Create and save user.
            user_id, uuid = self.user_obj.save_user(first_name=user[0],
                                                    last_name=user[1],
                                                    phone_number=user[2],
                                                    reg_id=reg_id,
                                                    external_user_id=user[3])

            # Create and save the user's role.
            self.user_obj.assign_role(user_id, PROVIDER)

            # Create and assign a provider, provider facility and provider role.
            provider_id = self.add_provider(user_id, facility_id, role, is_primary_provider)

            # return the id of the provider created.
            return provider_id

        except SQLAlchemyError as error:
            logging.error(str(error))
            raise InternalServerError(str(error))

    def add_provider(self, user_id, facility_id, role_name, is_primary_provider):
        exist_facility = Facilities.find_by_id(facility_id)
        # raise if invalid facility id was received
        if not exist_facility:
            raise NotFound(f"facility with id {facility_id} was not found")

        # raise if invalid role name was received
        role = ProviderRoleTypes.find_by_name(role_name)
        if not role:
            raise NotFound(
                f"could not find role with name {role} in provider_role_types"
            )

        # create and save provider
        provider = provider_schema.load(
            {"user_id": user_id, "facility_id": facility_id, "is_primary": is_primary_provider}
        )
        logging.info(f"Saving provider in the database {provider.__dict__}")
        self.flush_db(provider)
        self.commit_db()
        # provider.save_to_db()

        # raise if provider was not saved
        if not provider.id:
            raise NotFound(
                f"provider with user_id {user_id} and facility_id {facility_id} was not created"
            )

        # assign a provider role to the provider
        provider_role = provider_role_schema.load(
            {"provider_role_id": role.id, "provider_id": provider.id}
        )
        logging.info(f"Saving provider role in the database")
        self.flush_db(provider_role)
        self.commit_db()
        # provider_role.save_to_db()

        return provider.id

    def report_signed_link(self, report_id):
        from utils.common import generate_signed_url

        key = (
            db.session.query(Salvos.pdf_location)
            .filter(Salvos.id == report_id)
            .scalar()
        )
        if key is None:
            return "No report found", 404
        signed_url = generate_signed_url(report_key=key)
        return signed_url, 200

    def update_uploaded_ts(self, report_id):
        if report_id is None:
            return "reportId is None", 404
        salvos = (
            db.session.query(Salvos)
            .filter(Salvos.therapy_report_id == report_id)
            .first()
        )
        if salvos is None:
            return "not found", 404
        salvos.clinician_verified_at = datetime.now()
        self.save_db(salvos)
        return "updated data", 201

    def patient_detail_byid(self, patient_id):
        base_query = (
            db.session.query(Patient)
            .filter(Patient.id == patient_id)
            .join(Users, Users.id == Patient.user_id)
            .join(UserRegister, UserRegister.id == Users.registration_id)
            .join(UserStatus, Users.id == UserStatus.user_id, isouter=True)
            .join(
                UserStatusType, UserStatus.status_id == UserStatusType.id, isouter=True,
            )
        )

        patient_data = (
            base_query.join(Address, Patient.permanent_address_id == Address.id, isouter=True)
            .join(TherapyReport, Patient.id == TherapyReport.patient_id, isouter=True)
            .with_entities(
                Patient.id,
                UserRegister.email,
                Users.first_name,
                Users.last_name,
                Users.phone_number,
                Patient.date_of_birth,
                Patient.enrolled_date,
                Patient.unenrolled_at,
                Patient.emergency_contact_name,
                Patient.emergency_contact_number,
                Address.street_address_1,
                Address.street_address_2,
                Address.city,
                Address.state,
                Address.country,
                Address.postal_code,
                UserStatusType.name,
            )
            .first()
        )

        if patient_data is None:
            return {}, []
        reports = (
            db.session.query(TherapyReport, Salvos)
            .join(Salvos, TherapyReport.id == Salvos.therapy_report_id, isouter=True)
            .with_entities(
                Salvos.id, TherapyReport.created_at, Salvos.clinician_verified_at
            )
            .filter(TherapyReport.patient_id == patient_data[0])
            .order_by(Salvos.id)
            .all()
        )

        return patient_data, reports

    def patients_list(
        self,
        provider_id,
        page_number,
        record_per_page,
        first_name,
        last_name,
        date_of_birth,
        report_id,
    ):
        patient_list = namedtuple(
            "PatientList",
            (
                "id",
                "email",
                "first_name",
                "last_name",
                "mobile",
                "date_of_birth",
                "status",
                "reports",
            ),
        )
        base_query = self._base_query(provider_id)
        base_query = base_query.with_entities(
            Patient.id,
            UserRegister.email,
            Users.first_name,
            Users.last_name,
            Users.phone_number,
            Patient.date_of_birth,
            UserStatusType.name,
        )
        filter_query = self._filter_query(
            base_query, first_name, last_name, date_of_birth, report_id
        )
        data_count = filter_query.count()
        query_data = (
            filter_query.order_by(Users.first_name)
            .paginate(page_number + 1, record_per_page)
            .items
        )
        lists = []

        for data in query_data:
            reports = (
                db.session.query(TherapyReport.id)
                .filter(TherapyReport.patient_id == data[0])
                .all()
            )
            reports = [report[0] for report in reports]
            patient_data = patient_list(*data, reports)
            lists.append(patient_data._asdict())

        return lists, data_count

    def list_all_patients_by_provider(self, provider_id):
        """List all patients records given provider_id"""
        logging.debug(f"List all patients for provider: {provider_id}")
        try:
            patients_providers = PatientsProviders.find_by_provider_id(provider_id)
            patients_list = []

            for patient_provider in patients_providers:
                print(f"provider: {provider_id} with patient: {patient_provider.patient_id}")

                patient = {}
                patient_record = Patient.find_by_id(patient_provider.patient_id)
                user_record = Users.find_by_patient_id(patient_record.user_id)
                patient["id"] = patient_provider.patient_id
                patient["first_name"] = user_record.first_name
                patient["last_name"] = user_record.last_name
                # patients_dict[provider_id].append(patient)
                patients_list.append(patient)

            return patients_list
        except exc.SQLAlchemyError as error:
            logging.error("Error occured: {}".format(str(error)))
            raise InternalServerError(str(error))

    def _base_query(self, provider_id):
        """
        :return := Return the base query for patient list
        """
        patient_query = (
            db.session.query(Patient).distinct()
            .join(PatientsProviders, Patient.id == PatientsProviders.patient_id)
            .filter(PatientsProviders.provider_id == provider_id)
        )

        base_query = (
            patient_query.join(Users, Users.id == Patient.user_id)
            .join(UserRegister, UserRegister.id == Users.registration_id)
            .join(UserStatus, Users.id == UserStatus.user_id, isouter=True)
            .join(
                UserStatusType, UserStatus.status_id == UserStatusType.id, isouter=True,
            )
        )

        return base_query

    def _filter_query(
        self, base_query, first_name, last_name, date_of_birth, report_id
    ):
        if report_id is not None and report_id != 0:
            patient_id = (
                db.session.query(TherapyReport.patient_id)
                .filter(TherapyReport.id == report_id)
                .scalar()
            )
            if patient_id is None:
                raise NotFound("report not found")
            else:
                base_query = base_query.filter(Patient.id == patient_id)

        if first_name is not None and len(first_name) > 0:
            first_name = "%{}%".format(first_name)
            base_query = base_query.filter(Users.first_name.ilike(first_name))

        if last_name is not None and len(last_name) > 0:
            last_name = "%{}%".format(last_name)
            base_query = base_query.filter(Users.last_name.ilike(last_name))

        if date_of_birth is not None and len(date_of_birth):
            base_query = base_query.filter(Patient.date_of_birth == date_of_birth)

        return base_query

    def update_provider(self, facility_id, user, email, provider_from_db):
        """
        Updating providers will affect 3 tables on following checks
            - providers:    if the facility id is different from the data in DB.
            - users:        if the first name, last name, phone number or external user id is different from data in
                            users table
            - registration: if the email is different from the email in registrations table

            If the registration email changes (Security):
                - Update database with the new email.
                - Generate a new password and update the database with the new password
                - the registration email needs to be resent with a new password.
        """
        session = db.session
        try:
            user_id = provider_from_db.user_id

            # 1.check if the facility id is the same from what was in the database
            # Facility id can not be NULL.
            if int(facility_id) != provider_from_db.facility_id:
                logging.debug("Facility_ids are different")
                provider_from_db.facility_id = facility_id
                provider_from_db.updated_on = datetime.now()
                session.add(provider_from_db)

            # 2. check if the user object has any changes
            user_from_db = Users.find_by_id(_id=user_id)
            if user_from_db is None:
                raise InternalServerError(f"User with {user_id} not found")

            updated, user_from_db = self.update_user(user_from_db, user)
            if updated:
                logging.debug("user data is modified")
                user_from_db.updated_on = datetime.now()
                session.add(user_from_db)

            # 3.Check registration
            registration = UserRegister.find_by_id(user_from_db.registration_id)
            if registration is None:
                raise InternalServerError(f"Registration info for user {user_id} not found")

            registration_updated = False
            pwd = None
            if registration.email != email:
                logging.debug(f"registration email {registration.email} is different from email in req {email}")
                # check if any other user account exists with the same email - Emails are unique
                duplicate_email = UserRegister.find_by_email(email)
                if duplicate_email:
                    raise InternalServerError(f"Another user with the email {email} already exists")
                else:
                    registration.email = email
                    pwd = generate_random_password()
                    registration.password = encPass(pwd)
                    registration.updated_at = datetime.now()
                    session.add(registration)
                    registration_updated = True

            session.commit()

            # send registration email to the new email address
            if registration_updated:
                logging.info("Sending an email notification to the new address")
                send_provider_registration_email(
                    first_name=user.first_name,
                    last_name=user.last_name,
                    to_address=registration.email,
                    username=registration.email,
                    password=pwd
                )
        except Exception as ex:
            session.rollback()
            logging.error("Error occurred: {}".format(str(ex)))
            raise InternalServerError(str(ex))

    def update_user(self, user_from_db, user_from_req):
        updated = False

        if user_from_db.first_name != user_from_req.first_name:
            user_from_db.first_name = user_from_req.first_name
            updated = True

        if user_from_db.last_name !=  user_from_req.last_name:
            user_from_db.last_name = user_from_req.last_name
            updated = True

        if user_from_db.phone_number != user_from_req.phone_number:
            user_from_db.phone_number = user_from_req.phone_number
            updated = True

        if user_from_db.external_user_id != user_from_req.external_user_id:
            user_from_db.external_user_id = user_from_req.external_user_id
            updated = True

        return updated, user_from_db

    def get_providers_list(self, page_number, record_per_page, name):
        provider_list = namedtuple(
            "ProviderList",
            (
                "provider_name",
                "id",
                "phone",
                "site_name",
                "email_address"
            )
        )
        base_query = self._base_provider_query(name)
        base_query = base_query.with_entities(
            Users.first_name,
            Users.last_name,
            Providers.id,
            Users.phone_number,
            UserRegister.email,
            Facilities.name
        )

        data_count = base_query.count()
        query_data = []
        lists = []

        try:
            query_data = (
                base_query.order_by(Users.first_name).paginate(page_number + 1, record_per_page).items
            )
        except Exception as e:
            logging.exception(e)

        for data in query_data:
            provider = provider_list(
                provider_name=data[0] + " " + data[1],
                id=data[2],
                phone=data[3],
                site_name=data[5],
                email_address=data[4]
            )
            lists.append(provider._asdict())

        return lists, data_count

    def _base_provider_query(self, name):
        """
        :return := Return the base query for patient list
        """
        provider_query = (db.session.query(Providers))
        provider_query = (
            provider_query.join(Users, Users.id == Providers.user_id)
            .join(UserRegister, UserRegister.id == Users.registration_id)
            .join(UserStatus, Users.id == UserStatus.user_id, isouter=True)
            .join(UserStatusType, UserStatus.status_id == UserStatusType.id, isouter=True)
            .join(Facilities, Providers.facility_id == Facilities.id, isouter=True)
        )

        if name is not None and len(name) > 0:
            provider_query = provider_query.filter(Users.first_name.ilike(name) | Users.last_name.ilike(name))

        return provider_query
