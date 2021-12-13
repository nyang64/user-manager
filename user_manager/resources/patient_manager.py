import http
import logging
import json

from flask import jsonify, request
from model.address import Address
from model.facilities import Facilities
from model.patient import Patient
from model.patients_devices import PatientsDevices
from model.patients_patches import PatientsPatches
from schema.patient_details_schema import PatientDetailsSchema
from model.patients_providers import PatientsProviders
from model.provider_role_types import ProviderRoleTypes
from model.providers import Providers
from model.user_registration import UserRegister
from model.users import Users
from model.user_status_type import UserStatusType
from schema.address_schema import AddressSchema
from schema.patient_schema import (
    PatientSchema,
    assign_device_schema,
    assign_patches_schema,
    create_patient_schema,
    update_patient_schema,
    patient_list_schema,
    deactivate_patient_schema
)
from schema.patient_schema import patients_schema
from schema.patients_devices_schema import PatientsDevicesSchema
from schema.patient_details_schema import PatientDetails
from schema.providers_schema import ProvidersSchema
from schema.register_schema import RegistrationSchema
from schema.user_schema import UserSchema
from services.patient_services import PatientServices
from services.material_request_services import MaterialRequestService
from utils.constants import ADMIN, PATIENT, PROVIDER, CUSTOMER_SERVICE, STUDY_MANAGER, ENROLLED, DISENROLLED
from utils.common import generate_random_password, have_keys
from utils.jwt import require_user_token
from utils.validation import validate_request
from werkzeug.exceptions import BadRequest


class PatientManager:
    def __init__(self):
        self.patient_obj = PatientServices()

    @require_user_token(ADMIN, STUDY_MANAGER, CUSTOMER_SERVICE, PROVIDER)
    def create_patient(self, token):
        from utils.send_mail import send_patient_registration_email

        request_params = validate_request()
        logging.debug(
            "User: {} with role: {} - is registering a new patient: {}::{}".format(token["user_email"],
                                                                                   token["user_role"],
                                                                                   request_params["first_name"],
                                                                                   request_params["last_name"]))

        pwd = generate_random_password()
        request_params["password"] = pwd
        request_params["role_name"] = "PATIENT"

        register_params, user_params, patient_params = create_patient_schema.load(
            request_params
        )

        # check if the device is already assigned to a patient before registering the patient
        device_in_use = False
        if request_params.get("device_serial_number"):
            device_in_use = PatientsDevices.device_in_use(request_params["device_serial_number"])

        if device_in_use:
            raise Exception("Device is already in use")

        patient_id = self.patient_obj.register_patient(register_params, user_params, patient_params)
        send_patient_registration_email(
            user_params[0],
            register_params[0],
            "Welcome to Element Science",
            register_params[0],
            register_params[1],
        )

        if request_params.get("device_serial_number"):
            self.assign_first_device(patient_id, request_params["device_serial_number"])

        if patient_params.get("patches") is not None:
            self.assign_patches(patient_id, patient_params["patches"])

        patient_schema = PatientSchema()
        patient = Patient.find_by_id(patient_id)

        prs = MaterialRequestService()
        prs.send_initial_product_request(token["user_email"], patient, register_params[0])

        return jsonify(patient_schema.dump(patient)), http.client.CREATED


    def assign_first_device(self, patient_id, device_serial_number):
        """
            Assign the first device to a patient
        """
        patient_device = assign_device_schema.load(
            {"device_serial_number": device_serial_number, "patient_id": patient_id}
        )
        return self.patient_obj.assign_device_to_patient(patient_device)

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

        return self.patient_obj.save_patient_patches(patches_to_persist)

    @require_user_token(ADMIN, CUSTOMER_SERVICE, STUDY_MANAGER, PROVIDER)
    def update_patient(self, token):
        patient_id = request.args.get("id")
        if patient_id is None:
            raise BadRequest("parameter id is missing")
        request_data = validate_request()

        try:
            patient_data_from_db = Patient.find_by_id(_id=patient_id)
            if patient_data_from_db is None:
                return {"message": "No such patient exist"}, 404
            user, email, patient, patient_details = update_patient_schema.load(request_data)
            self.patient_obj.update_patient_data(
                user, email, patient, patient_details, patient_data_from_db
            )
        except Exception as ex:
            return {"message": ex.description}, http.client.BAD_REQUEST

        return {"message": "Successfully updated"}, http.client.OK

    @require_user_token(ADMIN, CUSTOMER_SERVICE, STUDY_MANAGER)
    def delete_patient(self, token):
        try:
            request_data = validate_request()
            patient_id, deactivation_reason, deactivation_notes = deactivate_patient_schema.load(request_data)
            self.patient_obj.delete_patient_data(patient_id, deactivation_reason, deactivation_notes)
        except Exception as e:
            print(e)
            return {"message": str(e)}, http.client.BAD_REQUEST

        return {"message": "Patient deleted"}, http.client.OK

    @require_user_token(ADMIN, PROVIDER, CUSTOMER_SERVICE, STUDY_MANAGER)
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

    @require_user_token(ADMIN, CUSTOMER_SERVICE, STUDY_MANAGER, PROVIDER)
    def patients_list(self, token):
        """
        :param :- page_number, record_per_page, name, external ID, site id, provider id, status
        :return filtered patient list
        """
        request_data = validate_request()
        logging.debug(
            "User: {} with role: {} - is requesting a list of patients".format(token["user_email"],
                                                                                   token["user_role"]))
        filter_input = patient_list_schema.load(request_data)
        patients_list, total = self.patient_obj.get_patients_list(*filter_input)

        return (
            {
                "total": total,
                "page_number": filter_input[0],
                "record_per_page": filter_input[1],
                "data": patients_list,
                "status_code": http.client.OK,
            },
            http.client.OK,
        )

    @require_user_token(ADMIN, CUSTOMER_SERVICE, STUDY_MANAGER, PROVIDER)
    def get_patient_by_id(self, token):
        # TODO Add more logic to get all needed data
        patient_id = request.args.get("id")
        patient_data = Patient.find_by_id(patient_id)
        if patient_id is None:
            return {"message": "No Such Patient Exist"}, 404

        patient_data_json = patient_data.__dict__
        del patient_data_json["_sa_instance_state"]
        return {"message": "Users Found", "Data": [patient_data_json]}, 200

    @require_user_token(ADMIN, CUSTOMER_SERVICE, STUDY_MANAGER, PROVIDER)
    def get_patient_details_by_id(self, token):
        patient_id = request.args.get("id")
        patient_data = Patient.find_by_id(patient_id)
        if patient_id is None:
            return {"message": "No Such Patient Exist"}, 404

        details = PatientDetails.find_by_patient_id(patient_id)
        details_json = PatientDetailsSchema().dump(details)
        patient_json = PatientSchema().dump(patient_data)

        # Get the notes and deactivation reason
        enrolled_status = UserStatusType.find_by_name(ENROLLED)
        disenrolled_status = UserStatusType.find_by_name(DISENROLLED)
        for status in patient_data.user.statuses:
            if status.status_id == enrolled_status.id:
                patient_json["enrollment_notes"] = status.notes
            elif status.status_id == disenrolled_status.id:
                patient_json["deactivation_reason"] = json.loads(status.deactivation_reason)
                patient_json["deactivation_notes"] = status.notes


        # TODO: Write a single query to get all these data from the database in one call
        # outpatient provider
        outpatient_role_id = ProviderRoleTypes.find_by_name(_name="outpatient").id
        outpatient_provider = PatientsProviders.find_by_patient_and_role_id(
            patient_data.id, outpatient_role_id
        )

        # prescribing provider
        prescribing_role_id = ProviderRoleTypes.find_by_name(_name="prescribing").id
        prescribing_provider = PatientsProviders.find_by_patient_and_role_id(
            patient_data.id, prescribing_role_id
        )

        response = {
            "patient": {
                "patient": patient_json,
                "outpatient_provider": outpatient_provider.provider_id,
                "prescribing_provider": prescribing_provider.provider_id,
                "details": details_json
            }
        }
        return jsonify(response), 200


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

        # PATCH FOR THERAPY REPORT - REPORT_GENERATOR NEEDS TO BE UPDATED AND USE "PERMANENT_ADDRESS" KEY INSTEAD
        # OF "ADDRESS" KEY IN PATIENT SCHEMA JSON
        patient_json = patient_schema.dump(patient)
        patient_json["address"] = patient_json.pop("permanent_address")

        response = {
            "patient": {
                "patient": patient_json,
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
