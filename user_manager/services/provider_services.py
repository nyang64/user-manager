import logging
from collections import namedtuple

from db import db
from model.address import Address
from model.facilities import Facilities
from model.patient import Patient
from model.patients_providers import PatientsProviders
from model.provider_role_types import ProviderRoleTypes
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
from werkzeug.exceptions import InternalServerError, NotFound

provider_role_schema = ProvidersRolesSchema()
provider_schema = ProvidersSchema()


class ProviderService(DbRepository):
    def __init__(self):
        self.auth_obj = AuthServices()
        self.user_obj = UserServices()

    def register_provider_service(self, register, user, facility_id, role):
        try:
            # Save data in the registration table
            reg_id = self.auth_obj.register_new_user(register[0], register[1])

            # Create and save user.
            user_id, uuid = self.user_obj.save_user(user[0], user[1], user[2], reg_id)

            # Create and save the user's role.
            self.user_obj.assign_role(user_id, PROVIDER)

            # Create and assign a provider, provider facility and provider role.
            provider_id = self.add_provider(user_id, facility_id, role)

            # return the id of the provider created.
            return provider_id

        except SQLAlchemyError as error:
            logging.error(str(error))
            raise InternalServerError(str(error))

    def add_provider(self, user_id, facility_id, role_name):
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
            {"user_id": user_id, "facility_id": facility_id}
        )
        provider.save_to_db()

        # raise if provider was not saved
        if not provider.id:
            raise NotFound(
                f"provider with user_id {user_id} and facility_id {facility_id} was not created"
            )

        # assign a provider role to the provider
        provider_role = provider_role_schema.load(
            {"provider_role_id": role.id, "provider_id": provider.id}
        )
        provider_role.save_to_db()

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
        from datetime import datetime

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
            base_query.join(Address, Users.id == Address.user_id, isouter=True)
            .join(TherapyReport, Patient.id == TherapyReport.patient_id, isouter=True)
            .with_entities(
                Patient.id,
                UserRegister.email,
                Users.first_name,
                Users.last_name,
                Users.phone_number,
                Patient.date_of_birth,
                Patient.enrolled_date,
                Patient.emergency_contact_name,
                Patient.emergency_contact_number,
                Address.street_address_1,
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

    def _base_query(self, provider_id):
        """
        :return := Return the base query for patient list
        """
        patient_query = (
            db.session.query(Patient)
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
