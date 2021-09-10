from datetime import datetime
import logging

from db import db
from model.patient import Patient
from model.patients_devices import PatientsDevices
from model.provider_role_types import ProviderRoleTypes
from model.user_registration import UserRegister
from model.users import Users
from model.address import Address
from model.patients_providers import PatientsProviders
from model.newsletters import Newsletters
from schema.newsletter_schema import NewsletterSchema
from schema.patients_providers_schema import PatientsProvidersSchema
from services.auth_services import AuthServices
from services.device_manager_api import DeviceManagerApi
from services.repository.db_repositories import DbRepository
from services.user_services import UserServices
from werkzeug.exceptions import Conflict, InternalServerError, NotAcceptable, NotFound

from utils.common import generate_random_password, encPass
from utils.send_mail import send_patient_registration_email


class PatientServices(DbRepository):
    def __init__(self):
        self.auth_obj = AuthServices()
        self.user_obj = UserServices()

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
                "day_at": 0,
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
                        device_serial_number
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
        patient_device.is_active = False
        self.flush_db(patient_device)
        self.commit_db()
        return patient_device.patient_id

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

            session.commit()
        except Exception as ex:
            session.rollback()
            logging.error("Error occurred: {}".format(str(ex)))
            raise InternalServerError(str(ex))

    def delete_patient_data(self, patient_id):
        exist_patient = Patient.find_by_id(patient_id)
        if bool(exist_patient) is False:
            raise NotFound("patient record not found")

        # Unenroll patient from patients table
        exist_patient.unenrolled_at = datetime.now()
        self.save_db(exist_patient)

        # Proceed to soft delete from user table
        self.user_obj.delete_user_byid(exist_patient.user_id)

    # TODO: Consolidate this in the user schema/model
    def __update_user(self, user_from_db, user_from_req):
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

    def __check_patient_device_association(self, session, new_sn, patient_id, patient_devices):
        if patient_devices.device_serial_number == new_sn:
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
                        # Set the current device to not active
                        patient_devices.is_active = False
                        patient_devices.updated_on = datetime.now()

                        session.add(patient_devices)
                        session.add(patient_device_new)

                        DeviceManagerApi.update_device_status(new_sn)
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


