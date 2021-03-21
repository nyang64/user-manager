from seeds import users
from seeds.helpers import print_message_details, message_details

from utils.constants import PATIENTS

from model.patients_providers import PatientsProviders
from model.patients_devices import PatientsDevices

from schema.patient_schema import PatientSchema
from schema.patients_devices_schema import PatientsDevicesSchema
from schema.patients_providers_schema import PatientsProvidersSchema
from model.providers import Providers

patient_schema = PatientSchema()


def seed(outpatient_provider, prescribing_provider):
    for patient_details in PATIENTS:
        create_patient(patient_details, outpatient_provider, prescribing_provider)


def create_patient(patient_details, outpatient_provider, prescribing_provider):
    registered_user_id = users.create_and_register_user(patient_details)
    patient_details = patient_details["patient"]

    patient = patient_schema.load({
        "emergency_contact_name": patient_details["emergency_contact_name"],
        "emergency_contact_number": patient_details["emergency_contact_phone"],
        "date_of_birth": patient_details["date_of_birth"],
        "gender": patient_details["gender"],
        "provider_id": prescribing_provider.id,
        "user_id": registered_user_id
    })

    patient.save_to_db()
    message_details["patient"] += f"Patient with id '{patient.id}' created with user id {id}. "
    create_patient_device(patient.id, "12345678")
    create_patient_provider(patient.id, prescribing_provider, 1)
    create_patient_provider(patient.id, outpatient_provider, 2)

    print_message_details()

    return patient.id
    # else:
    #     message_details["patient"] += "Patient was not added. "


def create_patient_device(patient_id, serial_number):
    patient_device_schema = PatientsDevicesSchema()
    patient_device_details = {
        "patient_id": patient_id,
        "device_id": serial_number
    }

    patient_device = patient_device_schema.load(patient_device_details)
    patient_device.save_to_db()

    message_details["patient"] += f"Patient with id '{patient_id}' was associated with device serial number {serial_number}. "


def create_patient_provider(patient_id, provider, role_id):
    patient_provider_schema = PatientsProvidersSchema()
    patient_provider = patient_provider_schema.load(
        {
            "patient_id": patient_id,
            "provider_id": provider.id,
            "provider_role_id": role_id
        }
    )

    patient_provider.save_to_db()
    message_details["patient"] += f"Patient with id '{patient_id}' was associated with provider id {provider.id}. "
    print_message_details()
