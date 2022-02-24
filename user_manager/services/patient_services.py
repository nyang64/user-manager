from collections import namedtuple
from datetime import datetime
import logging

from db import db
from model.facilities import Facilities
from model.therapy_reports import TherapyReport
from model.patient import Patient
from model.patients_devices import PatientsDevices
from model.patients_patches import PatientsPatches
from model.provider_role_types import ProviderRoleTypes
from model.user_registration import UserRegister
from model.users import Users
from model.user_status import UserStatus
from model.user_status_type import UserStatusType
from model.address import Address
from model.patients_providers import PatientsProviders
from model.providers import Providers
from model.patient_details import PatientDetails
from model.newsletters import Newsletters
from schema.newsletter_schema import NewsletterSchema
from schema.patients_providers_schema import PatientsProvidersSchema
from schema.patient_schema import assign_patches_schema
from services.auth_services import AuthServices
from services.device_manager_api import DeviceManagerApi
from services.repository.db_repositories import DbRepository
from services.user_services import UserServices
from utils.constants import ASSIGNED, INACTIVE, PRESCRIBING_PROVIDER
from werkzeug.exceptions import Conflict, InternalServerError, NotFound

from utils.common import generate_random_password, encPass
from utils.send_mail import send_patient_registration_email


class PatientServices(DbRepository):
    def __init__(self):
        self.auth_obj = AuthServices()
        self.user_obj = UserServices()
        self.newsletter_start_day = 0

    def register_patient(self, register, user, patient_details):
        """
            Register a patient record in the system
            This function will update the following tables:
            - registration
            - address
            - users
            - patients
            - patients and providers

            This function also enrolls the users to receive newsletters
        """
        user_id, user_uuid = self.user_obj.register_user(register, user)
        patient_details["patient"]["user_id"] = user_id

        if patient_details["patient"]["permanent_address"]:
            patient_details["patient"]["permanent_address_id"] = self.save_address(
                patient_details["patient"]["permanent_address"]
            )

        # Check if shipping address exists if not same as permanent address
        if "shipping_address" in patient_details["patient"].keys():
            if patient_details["patient"]["shipping_address"]:
                patient_details["patient"]["shipping_address_id"] = self.save_address(
                    patient_details["patient"]["shipping_address"]
                )
            else:
                patient_details["patient"]["shipping_address"] = patient_details["patient"]["permanent_address"]
                patient_details["patient"]["shipping_address_id"] = patient_details["patient"]["permanent_address_id"]
        else:
            patient_details["patient"]["shipping_address"] = patient_details["patient"]["permanent_address"]
            patient_details["patient"]["shipping_address_id"] = patient_details["patient"]["permanent_address_id"]

        patient_id = self.save_patient(patient_details["patient"])

        self._save_patient_details(patient_id, patient_details["details"])

        self.assign_providers(
            patient_id,
            patient_details["providers"]["outpatient_provider_id"],
            patient_details["providers"]["prescribing_provider_id"],
        )

        self.enroll_newsletter(user_id)

        return patient_id

    def enroll_newsletter(self, user_id):
        user_newsletter_schema = NewsletterSchema()
        user_newsletter = user_newsletter_schema.load(
            {
                "user_id": user_id,
                "day_at": self.newsletter_start_day,
            }
        )
        self.flush_db(user_newsletter)
        self.commit_db()

    def assign_providers(
            self, patient_id, outpatient_provider_id, prescribing_provider_id
    ):
        prescribing_role = ProviderRoleTypes.find_by_name("prescribing")
        outpatient_role = ProviderRoleTypes.find_by_name("outpatient")
        patient_provider_schema = PatientsProvidersSchema()

        out_patient_provider = patient_provider_schema.load(
            {
                "patient_id": patient_id,
                "provider_id": outpatient_provider_id,
                "provider_role_id": outpatient_role.id,
            }
        )

        pre_patient_provider = patient_provider_schema.load(
            {
                "patient_id": patient_id,
                "provider_id": prescribing_provider_id,
                "provider_role_id": prescribing_role.id,
            }
        )

        self.flush_db(out_patient_provider)
        self.flush_db(pre_patient_provider)
        self.commit_db()

    def save_patient(self, patient_details):
        Users.check_user_exist(patient_details["user_id"])

        patient = Patient(**patient_details)
        self.flush_db(patient)
        self.commit_db()

        return patient.id

    def _save_patient_details(self, patient_id, patient_details):
        patient_details = PatientDetails(**patient_details)
        patient_details.patient_id = patient_id
        self.flush_db(patient_details)
        self.commit_db()

    def save_address(self, address):
        self.flush_db(address)
        self.commit_db()

        return address.id

    def count_device_assigned(self, patient_id):
        devices = (
            db.session.query(PatientsDevices.device_serial_number)
                .filter(PatientsDevices.patient_id == patient_id)
                .all()
        )

        assigned_count = len(devices)

        # why do we need to check device manager here? couldn't we use the count within user-manager?
        if assigned_count > 2:
            assigned_count = 0

            for device in devices:
                device_status = DeviceManagerApi.get_device_status(device[0])

                if device_status == "assigned":
                    assigned_count += 1

                logging.info(
                    f"{assigned_count} devices are assigned to patient id {patient_id}."
                )

        return assigned_count

    def save_patient_patches(self, patient_patches):
        for patient_patch in patient_patches:
            patient_patch.save_to_db()

    def assign_device_to_patient(self, patient_device):
        exist_patient = Patient.find_by_id(patient_device.patient_id)
        device_serial_number = patient_device.device_serial_number

        if not exist_patient:
            raise NotFound("patient record not found")

        device_in_use = PatientsDevices.device_in_use(
            patient_device.device_serial_number
        )

        if not device_in_use:
            device_count = self.count_device_assigned(patient_device.patient_id)

            if device_count <= 2:
                device_exists_in_dm = DeviceManagerApi.check_device_exists(
                    patient_device.device_serial_number
                )

                if device_exists_in_dm is True:
                    self.flush_db(patient_device)
                    updated = DeviceManagerApi.update_device_status(
                        device_serial_number,
                        ASSIGNED
                    )

                    if updated:
                        patient_device.save_to_db()
                        return patient_device
                else:
                    raise NotFound("Device record not found")
        else:
            raise Conflict("Device already associated with patient")

    def remove_patient_device_association(self, device_serial_number):
        patient_device = PatientsDevices.find_by_device_serial_number(device_serial_number)
        if patient_device is None:
            return None

        # Update patients_device association table
        patient_device.is_active = False
        self.flush_db(patient_device)

        # Update device manager table
        device_exists_in_dm = DeviceManagerApi.check_device_exists(
            device_serial_number
        )

        if device_exists_in_dm:
            updated = DeviceManagerApi.update_device_status(
                device_serial_number, INACTIVE
            )
            if updated:
                return patient_device.patient_id
        else:
            raise NotFound("Device record not found in device database")

    def patient_device_list(self, token):
        from sqlalchemy import and_

        serial_numbers_query = (
            db.session.query(Users)
                .join(
                UserRegister,
                and_(
                    UserRegister.id == Users.registration_id,
                    UserRegister.email == token.get("user_email"),
                ),
            )
                .join(Patient, Users.id == Patient.user_id)
                .join(PatientsDevices, Patient.id == PatientsDevices.patient_id)
                .with_entities(PatientsDevices.device_serial_number, Users.id)
        )
        device_serial_numbers = serial_numbers_query.filter_by(is_active=True).all()
        devices = []

        for d in device_serial_numbers:
            device = DeviceManagerApi.get_device(d[0])
            devices.append(device)

        return devices

    def update_patient_data(self, user, email, patient, patient_details, patient_data_from_db):
        """
        Updating patients will affect the following tables
            - users: if the first name, last name, phone number or external user id is different from data in
                            users table
            - patients: if any of the patients data changes
            - registration: if the email is different from the email in registrations table
            - patients-devices: if the device is different from the current device
            - address:
            - patient-providers:
            - patient-patches:
            - patient-details

            If the registration email changes (Security):
                - Update database with the new email.
                - Generate a new password and update the database with the new password
                - the registration email needs to be resent with a new password.
        """
        session = db.session
        try:
            user_id = patient_data_from_db.user_id

            # 1. check if the user object has any changes
            user_from_db = Users.find_by_id(_id=user_id)
            if user_from_db is None:
                raise InternalServerError(f"User with {user_id} not found")

            updated, user_from_db = self.__update_user(user_from_db, user)
            if updated:
                logging.debug("user data is modified")
                user_from_db.updated_on = datetime.now()
                session.add(user_from_db)

            # 2. Check if the email has changed
            # TODO: Move this to a common place
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

            # 3. Update patient information
            patient_data_from_db.copy(patient)
            patient_data_from_db.updated_at = datetime.now()
            session.add(patient_data_from_db)

            # 4. Check device association
            patient_devices = PatientsDevices.find_record_by_patient_id(patient_data_from_db.id)
            new_sn = patient_details["device"]["serial_number"]
            session = self.__check_patient_device_association(session, new_sn, patient_data_from_db.id, patient_devices)

            # 5. Check address
            session = self.__update_patient_address(session, patient, patient_data_from_db)

            # 6. Check on patient and provider association
            prescribing_role = ProviderRoleTypes.find_by_name("prescribing")
            outpatient_role = ProviderRoleTypes.find_by_name("outpatient")

            prescribing_provider_association = PatientsProviders.find_by_patient_and_role_id(
                _patient_id=patient_data_from_db.id,
                _role_id=prescribing_role.id)
            prescribing_provider_association.provider_id = patient_details["providers"]["prescribing_provider_id"]
            session.add(prescribing_provider_association)

            outpatient_provider_association = PatientsProviders.find_by_patient_and_role_id(
                _patient_id=patient_data_from_db.id,
                _role_id=outpatient_role.id)
            outpatient_provider_association.provider_id = patient_details["providers"]["outpatient_provider_id"]
            session.add(outpatient_provider_association)

            # 7. Update Patient details table
            session = self.__update_patient_details(session, patient_details["details"], patient_data_from_db.id)

            # 8. Update patients and patches
            session = self.__update_patch_details(session, patient_details["patches"], patient_data_from_db.id)

            session.commit()

            if registration_updated:
                logging.info("Sending an email notification to the new email address")
                send_patient_registration_email(user.first_name, email, "Welcome to Element Science",
                                                email, pwd)
        except Exception as ex:
            session.rollback()
            logging.error("Error occurred: {}".format(str(ex)))
            raise InternalServerError(str(ex))

    def delete_patient_data(self, patient_id, deactivation_reason, notes):
        exist_patient = Patient.find_by_id(patient_id)
        if bool(exist_patient) is False:
            raise NotFound("patient record not found")

        # Check if patient is already unenrolled
        if exist_patient.unenrolled_at:
            raise Conflict("patient already unenrolled")

        session = db.session
        try:
            # Unenroll patient from patients table
            exist_patient.unenrolled_at = datetime.now()
            session.add(exist_patient)

            # Proceed to soft delete from user table
            session = self.user_obj.delete_user_byid(exist_patient.user_id, deactivation_reason, notes, session)
            session.commit()
        except Exception as e:
            session.rollback()
            logging.error("Error occurred: {}".format(str(e)))
            raise InternalServerError(str(e))

    # TODO: Consolidate this in the user schema/model
    def __update_user(self, user_from_db, user_from_req):
        updated = False

        if user_from_db.first_name != user_from_req.first_name:
            user_from_db.first_name = user_from_req.first_name
            updated = True

        if user_from_db.last_name != user_from_req.last_name:
            user_from_db.last_name = user_from_req.last_name
            updated = True

        if user_from_db.phone_number != user_from_req.phone_number:
            user_from_db.phone_number = user_from_req.phone_number
            updated = True

        if user_from_db.external_user_id != user_from_req.external_user_id:
            user_from_db.external_user_id = user_from_req.external_user_id
            updated = True

        return updated, user_from_db

    def __check_patient_device_association(self, session, new_sn, patient_id, patient_devices):
        if patient_devices and patient_devices.device_serial_number == new_sn:
            logging.info("No new device is assigned")
        else:
            # check the device exists in the database and available
            device_in_use = PatientsDevices.find_by_device_serial_number(new_sn)

            if not device_in_use:
                device_count = self.count_device_assigned(patient_id)

                if device_count < 2:
                    device_exists_in_dm = DeviceManagerApi.check_device_exists(new_sn)

                    if device_exists_in_dm is True:
                        patient_device_new = PatientsDevices(
                            patient_id=patient_id,
                            device_serial_number=new_sn
                        )

                        # If patient_devices not None
                        if patient_devices:
                            # Set the current device to not active
                            patient_devices.is_active = False
                            patient_devices.updated_on = datetime.now()
                            session.add(patient_devices)

                        session.add(patient_device_new)

                        DeviceManagerApi.update_device_status(new_sn, ASSIGNED)
                    else:
                        raise NotFound("Device record not found")
            else:
                raise Conflict("Device already associated with patient")

        return session

    def __update_patient_address(self, session, patient_in, patient_from_db):
        perm_address_id = patient_from_db.permanent_address_id
        shipping_address_id = patient_from_db.shipping_address_id

        # Create a new address
        if perm_address_id is None:
            perm_address_id = self.save_address(patient_in["permanent_address"])
            patient_from_db.permanent_address_id = perm_address_id
            session.add(patient_from_db)
        else:
            perm_address = Address.find_by_id(perm_address_id)
            perm_address.copy(patient_in.permanent_address)
            perm_address.updated_on = datetime.now()
            session.add(perm_address)

        if perm_address_id == shipping_address_id:
            return session
        elif patient_in.shipping_address is None:
            patient_from_db.shipping_address_id = perm_address_id
            session.add(patient_from_db)
        else:
            ship_address = Address.find_by_id(shipping_address_id)
            ship_address.copy(patient_in.shipping_address)
            ship_address.updated_on = datetime.now()
            session.add(ship_address)

        return session

    def __update_patient_details(self, session, patient_details, patient_id):
        details_in_db = PatientDetails.find_by_patient_id(patient_id)
        details_in_db.update(**patient_details)
        session.add(details_in_db)
        return session

    def __update_patch_details(self, session, patches, patient_id):
        applied_patch_lot_number = patches["applied_patch_lot_number"]
        unused_patch_lot_number = patches["unused_patch_lot_number"]

        # check if the patch numbers were empty and return if no information was entered
        if (applied_patch_lot_number is None or len(applied_patch_lot_number) == 0) and \
                (unused_patch_lot_number is None or len(unused_patch_lot_number) == 0):
            return session

        updated_patches = []
        patches_in_db = PatientsPatches.find_by_patient_id(patient_id)
        if patches_in_db is None or len(patches_in_db) == 0:
            updated_patches = self.assign_patches(patient_id, patches)
        else:
            for patch in patches_in_db:
                if patch.is_applied is True:
                    patch.patch_lot_number = applied_patch_lot_number
                else:
                    patch.patch_lot_number = unused_patch_lot_number
                updated_patches.append(patch)
        for item in updated_patches:
            session.add(item)
        return session

    def assign_patches(self, patient_id, patches):
        patches_to_persist = []

        applied_patch_lot_number = patches["applied_patch_lot_number"]
        if applied_patch_lot_number is not None and len(applied_patch_lot_number) > 0:
            patient_patch_applied = assign_patches_schema.load(
                {
                    "patch_lot_number": applied_patch_lot_number,
                    "patient_id": patient_id,
                    "is_applied": True
                }
            )
            patches_to_persist.append(patient_patch_applied)

        unused_patch_lot_number = patches["unused_patch_lot_number"]
        if unused_patch_lot_number is not None and len(unused_patch_lot_number) > 0:
            patient_patch_unused = assign_patches_schema.load(
                {
                    "patch_lot_number": unused_patch_lot_number,
                    "patient_id": patient_id,
                    "is_applied": False
                }
            )
            patches_to_persist.append(patient_patch_unused)

        return patches_to_persist

    def get_enrollment_status(self, user_data) -> bool:
        patient = Patient.find_by_user_id(user_data.id)
        if patient:
            if patient.unenrolled_at:
                return False

        return True

    def get_patients_list(self, page_number, record_per_page, name, external_id, facility_id, provider_id, status):
        patient_list = namedtuple(
            "PatientList",
            (
                "name",
                "external_id",
                "provider_name",
                "enrolled_on",
                "site",
                "therapy_date",
                "patient_id",
                "enrollment_status",
                "reason",
                "primary_contact"
            )
        )

        base_query = self._base_query()
        base_query = base_query.with_entities(
            Users.external_user_id,
            Users.first_name,
            Users.last_name,
            UserStatusType.name,
            Patient.enrolled_date,
            TherapyReport.created_at,
            PatientsProviders.provider_id,
            Patient.id,
            UserStatus.deactivation_reason,
            Users.phone_number
        )

        filter_query = self._filter_query(base_query, name, external_id, status)
        data_count = filter_query.count()
        query_data = []
        lists = []

        try:
            if record_per_page == 0 and page_number == 0:
                query_data = (filter_query.order_by(Users.id, Users.first_name)).all()
            else:
                query_data = (
                    filter_query.order_by(Users.id, Users.first_name).
                        paginate(page_number + 1, record_per_page).items
                )
        except Exception as e:
            logging.exception(e)

        # For each of the patients get the prescribing providers and facility name
        # There will be only one facility associated with a provider
        if query_data is not None and len(query_data) > 0:
            for data in query_data:
                provider_facility = db.session.query(Users, Facilities, Providers) \
                    .join(Providers, Providers.user_id == Users.id) \
                    .join(Facilities, Providers.facility_id == Facilities.id) \
                    .filter(Providers.id == data[6]).all()

                user = provider_facility[0][0]
                facility = provider_facility[0][1]
                provider = provider_facility[0][2]

                add_to_list = True

                if 0 < facility_id != facility.id:
                    add_to_list = False

                if 0 < provider_id != provider.id:
                    add_to_list = False

                if add_to_list:
                    patient_data = patient_list(
                        name=data[1] + " " + data[2],
                        external_id=data[0],
                        therapy_date=data[5].strftime("%d-%b-%Y") if data[5] is not None else None,
                        enrolled_on=data[4].strftime("%d-%b-%Y"),
                        provider_name=user.first_name + " " + user.last_name,
                        site=facility.name,
                        patient_id=data[7],
                        enrollment_status=data[3],
                        reason=data[8],
                        primary_contact=data[9]
                    )

                    lists.append(patient_data._asdict())

        return lists, data_count

    def _base_query(self):
        """
        :return := Return the base query for patient list
        """
        patient_query = (db.session.query(Patient))

        base_query = (
            patient_query.join(Users, Users.id == Patient.user_id).distinct(Users.id)
                .join(UserRegister, UserRegister.id == Users.registration_id)
                .join(UserStatus, Users.id == UserStatus.user_id, isouter=True)
                .join(UserStatusType, UserStatus.status_id == UserStatusType.id, isouter=True)
                .join(PatientsProviders, PatientsProviders.patient_id == Patient.id, isouter=True)
                .join(TherapyReport, TherapyReport.patient_id == Patient.id, isouter=True)
        )

        return base_query

    def _filter_query(self, base_query, name, external_id, status):

        if external_id is not None and len(external_id) > 0:
            base_query = base_query.filter(Users.external_user_id == external_id)

        if name is not None and len(name) > 0:
            base_query = base_query.filter(Users.first_name.ilike(name) | Users.last_name.ilike(name))

        if status is not None and len(status) > 0:
            base_query = base_query.filter(UserStatusType.name.ilike(status))

        base_query = base_query.filter(PatientsProviders.provider_role_id ==
                                       ProviderRoleTypes.find_by_name(PRESCRIBING_PROVIDER).id)

        return base_query

    """
    """

    def get_patient_details(self, patient_id):

        patient_query = (db.session.query(Patient)).distinct().filter(Patient.id == patient_id)

        base_query = (
            patient_query.join(Users, Users.id == Patient.user_id)
                .join(UserRegister, UserRegister.id == Users.registration_id)
                .join(UserStatus, Users.id == UserStatus.user_id, isouter=True)
                .join(UserStatusType, UserStatus.status_id == UserStatusType.id, isouter=True)
                .join(PatientsProviders, PatientsProviders.patient_id == Patient.id, isouter=True)
                .join(PatientDetails, PatientDetails.patient_id == Patient.id, isouter=True)
                .join(PatientsDevices, PatientsDevices.patient_id == Patient.id, isouter=True)
                .join(PatientsPatches, PatientsPatches.patient_id == patient_id, isouter=True)
        )

        result = base_query.with_entities(
            Users.external_user_id,
            Users.first_name,
            Users.last_name,
            UserStatusType.name,
            Patient.enrolled_date,
            PatientsProviders.provider_id,
            Patient.id,
            Users.id

        ).all()
        
        return None

    def _patient_download_query(self):
        
            """
            :return := Return the base query for patient download
            """
            patient_query = (db.session.query(Patient))

            base_query = (
                patient_query.join(Users, Users.id == Patient.user_id)
                    .join(UserRegister, UserRegister.id == Users.registration_id)
                    .join(UserStatus, Users.id == UserStatus.user_id, isouter=True)
                    .join(UserStatusType, UserStatus.status_id == UserStatusType.id, isouter=True)
                    .join(PatientsProviders, PatientsProviders.patient_id == Patient.id, isouter=True)
                    .join(TherapyReport, TherapyReport.patient_id == Patient.id, isouter=True)
                    .join(PatientsDevices, PatientsDevices.patient_id == Patient.id, isouter=True)
            )

            return base_query

    def get_patients_download(self):
            patient_download = namedtuple(
                "PatientDownload",
                (
                    "patient_id",
                    "provider_name",
                    "enrolled_on",
                    "site",
                    "therapy_date",
                    "enrollment_status",
                    "name",
                    "device_serial_number",
                    "is_mobile_user"
                )
            )

            base_query = self._patient_download_query()
            base_query = base_query.with_entities(
                Patient.id,
                Patient.enrolled_date,
                TherapyReport.created_at,
                PatientsProviders.provider_id,
                UserStatusType.name,
                Users.first_name,
                Users.last_name,
                PatientsDevices.device_serial_number,
                Patient.mobile_app_user
            )

            name= ""
            external_id = ""
            status= ""

            filter_query = self._filter_query(base_query, name, external_id, status)
            query_data = []
            lists = []

            try:
                query_data = (filter_query.order_by(Users.id, Users.first_name)).all()
            except Exception as e:
                logging.exception(e)

        
            if query_data is not None and len(query_data) > 0:
                for data in query_data:
                    provider_facility = db.session.query(Users, Facilities, Providers) \
                        .join(Providers, Providers.user_id == Users.id) \
                        .join(Facilities, Providers.facility_id == Facilities.id) \
                        .filter(Providers.id == data[3]).all()

                    user = provider_facility[0][0]
                    facility = provider_facility[0][1]
                    provider = provider_facility[0][2]

                    patient_data = patient_download(
                        name=data[5] + " " + data[6],
                        therapy_date=data[2].strftime("%d-%b-%Y") if data[2] is not None else None,
                        enrolled_on=data[1].strftime("%d-%b-%Y"),
                        provider_name=user.first_name + " " + user.last_name,
                        site=facility.name,
                        patient_id=data[0],
                        enrollment_status=data[4], 
                        device_serial_number=data[7],
                        is_mobile_user=data[8]
                    )

                    lists.append(patient_data._asdict())

            return lists