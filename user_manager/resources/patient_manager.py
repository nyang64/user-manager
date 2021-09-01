import http

from flask import jsonify, request
from model.address import Address
from model.facilities import Facilities
from model.patient import Patient
from model.patients_devices import PatientsDevices
from model.patients_patches import PatientsPatches
from model.patients_providers import PatientsProviders
from model.providers import Providers
from model.user_registration import UserRegister
from model.users import Users
from schema.address_schema import AddressSchema
from schema.patient_schema import (
    PatientSchema,
    assign_device_schema,
    assign_patches_schema,
    create_patient_schema,
    update_patient_schema,
)
from schema.patients_devices_schema import PatientsDevicesSchema
from schema.providers_schema import ProvidersSchema
from schema.register_schema import RegistrationSchema
from schema.user_schema import UserSchema
from services.patient_services import PatientServices
from utils.constants import ADMIN, PATIENT, PROVIDER, CUSTOMER_SERVICE, STUDY_MANAGER
from utils.common import generate_random_password
from utils.jwt import require_user_token
from utils.validation import validate_request
from werkzeug.exceptions import BadRequest


class PatientManager:
    def __init__(self):
        self.patient_obj = PatientServices()

    @require_user_token(ADMIN, STUDY_MANAGER, CUSTOMER_SERVICE)
    def create_patient(self, token):
        from utils.send_mail import send_patient_registration_email

        request_params = validate_request()

        pwd = generate_random_password()
        request_params["password"] = pwd
        request_params["role_name"] = "PATIENT"

        register_params, user_params, patient_params = create_patient_schema.load(
            request_params
        )

        patient_id = self.patient_obj.register_patient(
            register_params, user_params, patient_params
        )

        pwd = generate_random_password()
        send_patient_registration_email(
            user_params[0],
            register_params[0],
            "Welcome to Element Science",
            register_params[0],
            register_params[1],
        )

        if request_params.get("device_serial_number"):
            self.assign_first_device(patient_id, request_params["device_serial_number"])

        if request_params.get("patches"):
            self.assign_patches(patient_id, request_params["patches"])

        patient_schema = PatientSchema()
        patient = Patient.find_by_id(patient_id)

        return jsonify(patient_schema.dump(patient)), http.client.CREATED

    def assign_first_device(self, patient_id, device_serial_number):
        patient_device = assign_device_schema.load(
            {"device_serial_number": device_serial_number, "patient_id": patient_id}
        )
        return self.patient_obj.assign_device_to_patient(patient_device)

    def assign_patches(self, patient_id, patches):
        patches_to_persist = []
        for patch in patches:
            patch_lot_number = patch["patch_lot_number"]
            patient_patch = assign_patches_schema.load(
                {"patch_lot_number": patch_lot_number, "patient_id": patient_id}
            )
            patches_to_persist.append(patient_patch)

        return self.patient_obj.save_patient_patches(patches_to_persist)

    @require_user_token(ADMIN, PROVIDER)
    def update_patient(self, decrypt):
        patient_id = request.args.get("id")
        if patient_id is None:
            raise BadRequest("parameter id is missing")
        request_data = validate_request()
        patient = update_patient_schema.load(request_data)
        self.patient_obj.update_patient_data(
            patient_id, patient[0], patient[1], patient[2]
        )
        return {"message": "Sucessfully updated"}, http.client.OK

    @require_user_token(ADMIN, PROVIDER)
    def delete_patient(self, decrypt):
        patient_id = request.args.get("id")
        if patient_id is None:
            raise BadRequest("parameter id is missing")
        self.patient_obj.delete_patient_data(patient_id)
        return {"message": "Patient deleted"}, http.client.OK

    @require_user_token(ADMIN, PROVIDER)
    def assign_device(self, decrypt):
        request_data = validate_request()
        print(request_data)
        patient_device = assign_device_schema.load(request_data)
        self.patient_obj.assign_device_to_patient(patient_device)
        return {"message": "Device assigned", "status_code": "201"}, http.client.CREATED

    @require_user_token(PATIENT, ADMIN, PROVIDER)
    def patient_device_list(self, token):
        device_list = self.patient_obj.patient_device_list(token)
        resp = {"devices": device_list}
        return jsonify(resp), http.client.OK

    @require_user_token(ADMIN, CUSTOMER_SERVICE, STUDY_MANAGER, PROVIDER)
    def patients(self, token):
        patient_schema = PatientSchema(many=True)
        patients = Patient.all()

        return jsonify(patient_schema.dump(patients))

    @require_user_token(ADMIN, PROVIDER)
    def patient_remove_device(self, token):
        device_sn = request.args.get("device_serial_number")
        if device_sn is None:
            raise BadRequest("device serial number missing")
        patient_id = self.patient_obj.remove_patient_device_association(device_sn)
        if patient_id is None:
            return {"message": f"Unable to find patient association with device: {device_sn}"}, http.client.NOT_FOUND
        return {"message": f"Patient: {patient_id} disassociated with device serial number {device_sn}"}, http.client.OK


    def therapy_report_details(self, patient_id):
        # create schemas for formatting the JSON response
        register_schema = RegistrationSchema()
        patient_schema = PatientSchema()
        address_schema = AddressSchema()
        user_schema = UserSchema()
        patient_device_schema = PatientsDevicesSchema()
        provider_schema = ProvidersSchema()

        # patient's personal information
        patient = Patient.find_by_id(patient_id)
        user = Users.find_by_patient_id(patient.user_id)
        registration = UserRegister.find_by_id(user.registration_id)
        # patient's current device
        patient_device = PatientsDevices.find_by_patient_id(patient.id)

        # outpatient_provider
        outpatient_role_id = 1
        out_patient_provider = PatientsProviders.find_by_patient_and_role_id(
            patient.id, outpatient_role_id
        )
        outpatient_provider = Providers.find_by_id(out_patient_provider.provider_id)
        outpatient_provider_user = Users.find_by_id(outpatient_provider.user_id)
        outpatient_facility = Facilities.find_by_id(outpatient_provider.facility_id)
        outpatient_address = Address.find_by_id(outpatient_facility.address_id)
        outpatient_registration = UserRegister.find_by_id(
            outpatient_provider_user.registration_id
        )

        # prescribing provider
        prescribing_role_id = 2
        pre_patient_provider = PatientsProviders.find_by_patient_and_role_id(
            patient.id, prescribing_role_id
        )
        prescribing_provider = Providers.find_by_id(pre_patient_provider.provider_id)
        prescribing_provider_user = Users.find_by_id(prescribing_provider.user_id)
        prescribing_facility = Facilities.find_by_id(prescribing_provider.facility_id)
        prescribing_address = Address.find_by_id(prescribing_facility.address_id)
        prescribing_registration = UserRegister.find_by_id(
            prescribing_provider_user.registration_id
        )

        response = {
            "patient": {
                "patient": patient_schema.dump(patient),
                "user": user_schema.dump(user),
                "registration": register_schema.dump(registration),
            },
            "device": patient_device_schema.dump(patient_device),
            "providers": {
                "outpatient": {
                    "registration": register_schema.dump(outpatient_registration),
                    "user": user_schema.dump(outpatient_provider_user),
                    "provider": provider_schema.dump(outpatient_provider),
                    "facility": {
                        "name": outpatient_facility.name,
                        "address": address_schema.dump(outpatient_address),
                        "on_call_phone": outpatient_facility.on_call_phone,
                    },
                },
                "prescribing": {
                    "registration": register_schema.dump(prescribing_registration),
                    "user": user_schema.dump(prescribing_provider_user),
                    "provider": provider_schema.dump(prescribing_provider),
                    "facility": {
                        "name": prescribing_facility.name,
                        "address": address_schema.dump(prescribing_address),
                        "on_call_phone": prescribing_facility.on_call_phone,
                    },
                },
            },
        }

        return jsonify(response)
