import logging

from db import db
from model.patient import Patient
from model.patients_devices import PatientsDevices
from model.provider_role_types import ProviderRoleTypes
from model.user_registration import UserRegister
from model.users import Users
from model.newsletters import Newsletters
from schema.newsletter_schema import NewsletterSchema
from schema.patients_providers_schema import PatientsProvidersSchema
from services.auth_services import AuthServices
from services.device_manager_api import DeviceManagerApi
from services.repository.db_repositories import DbRepository
from services.user_services import UserServices
from werkzeug.exceptions import Conflict, InternalServerError, NotAcceptable, NotFound


class PatientServices(DbRepository):
    def __init__(self):
        self.auth_obj = AuthServices()
        self.user_obj = UserServices()

    def register_patient(self, register, user, patient_details):
        user_id, user_uuid = self.user_obj.register_user(register, user)
        patient_details["patient"]["user_id"] = user_id

        if patient_details["patient"]["permanent_address"]:
            patient_details["patient"]["permanent_address_id"] = self.save_address(
                patient_details["patient"]["permanent_address"]
            )

        # Check if shipping address exists if not same as permanent address
        if patient_details["patient"]["shipping_address"]:
            patient_details["patient"]["shipping_address_id"] = self.save_address(
                patient_details["patient"]["shipping_address"]
            )

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

    def update_patient_data(self, patient_id, emer_contact_name, emer_contact_no, dob):
        exist_patient = Patient.find_by_id(patient_id)
        if bool(exist_patient) is False:
            raise NotFound("patient record not found")
        exist_patient.emergency_contact_name = emer_contact_name
        exist_patient.emergency_contact_number = emer_contact_no
        exist_patient.date_of_birth = dob
        self.update_db(exist_patient)

    def delete_patient_data(self, patient_id):
        exist_patient = Patient.find_by_id(patient_id)
        if bool(exist_patient) is False:
            raise NotFound("patient record not found")
        self.user_obj.delete_user_byid(exist_patient.user_id)
