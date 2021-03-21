from flask import jsonify, request
from werkzeug.exceptions import BadRequest
import http
from services.patient_services import PatientServices
from utils.validation import validate_request
from utils.jwt import require_user_token
from utils.constants import ADMIN, PROVIDER, PATIENT, PATIENT_2_DICTIONARY

from model.patient import Patient
from model.users import Users
from model.providers import Providers
from model.facilities import Facilities
from model.address import Address
from model.patients_devices import PatientsDevices
from model.patients_providers import PatientsProviders
from model.user_registration import UserRegister

from schema.patient_schema import PatientSchema
from schema.patients_devices_schema import PatientsDevicesSchema
from schema.providers_schema import ProvidersSchema
from schema.address_schema import AddressSchema
from schema.user_schema import UserSchema
from schema.register_schema import RegistrationSchema
from schema.address_schema import AddressSchema
from schema.patient_schema import (create_patient_schema,
                                   update_patient_schema,
                                   assign_device_schema,)


class PatientManager():
    def __init__(self):
        self.patient_obj = PatientServices()

    @require_user_token(ADMIN, PROVIDER)
    def create_patient(self, decrypt):
        from utils.send_mail import send_registration_email
        request_data = validate_request()
        register, user, patient = create_patient_schema.load(request_data)
        user_id, user_uuid, patient_id = self.patient_obj.register_patient(
            register, user, patient)
        if user_id is not None and user_uuid is not None:
            send_registration_email(user[0], register[0],
                                    'Welcome to Element Science',
                                    register[0], register[1])
        return {'message': 'Patient created',
                'data': {
                    'user_uuid': user_uuid,
                    'user_id': user_id,
                    'patient_id': patient_id
                    },
                'status_code': '201'}, http.client.CREATED

    @require_user_token(ADMIN, PROVIDER)
    def update_patient(self, decrypt):
        patient_id = request.args.get('id')
        if patient_id is None:
            raise BadRequest("parameter id is missing")
        request_data = validate_request()
        patient = update_patient_schema.load(request_data)
        self.patient_obj.update_patient_data(patient_id, patient[0],
                                             patient[1], patient[2])
        return {"message": "Sucessfully updated"}, http.client.OK

    @require_user_token(ADMIN, PROVIDER)
    def delete_patient(self, decrypt):
        patient_id = request.args.get('id')
        if patient_id is None:
            raise BadRequest("parameter id is missing")
        self.patient_obj.delete_patient_data(patient_id)
        return {"message": "Patient deleted"}, http.client.OK

    @require_user_token(ADMIN, PROVIDER)
    def assign_device(self, decrypt):
        request_data = validate_request()
        patient_device = assign_device_schema.load(request_data)
        self.patient_obj.assign_device_to_patient(patient_device)
        return {'message': 'Device assigned',
                'status_code': '201'}, http.client.CREATED

    @require_user_token(PATIENT, ADMIN, PROVIDER)
    def patient_device_list(self, token):
        device_list = self.patient_obj.patient_device_list(token)
        resp = {'devices': device_list}
        return jsonify(resp), http.client.OK

    def therapy_report_details(self, patient_id):
        # create schemas for formatting the JSON response
        address_schema = AddressSchema()
        address_details = PATIENT_2_DICTIONARY["address"]
        register_schema = RegistrationSchema()
        patient_schema = PatientSchema()
        address_schema = AddressSchema()
        user_schema = UserSchema()
        patient_device_schema = PatientsDevicesSchema()
        provider_schema = ProvidersSchema()

        # patient's personal information
        patient = Patient.find_by_id(patient_id)
        user = Users.find_by_patient_id(patient.user_id)
        address = Address.find_by_user_id(user.id)
        registration = UserRegister.find_by_id(user.registration_id)
        # patient's current device
        patient_device = PatientsDevices.find_by_patient_id(patient.id)
        address_details["user_id"] = user.id
        address = address_schema.load(address_details)
        address.save_to_db()

        # outpatient_provider
        outpatient_role_id = 1
        out_patient_provider = PatientsProviders.find_by_patient_and_role_id(patient.id, outpatient_role_id)
        outpatient_provider = Providers.find_by_id(out_patient_provider.id)
        outpatient_provider_user = Users.find_by_user_id(outpatient_provider.user_id)
        outpatient_facility = Facilities.find_by_id(outpatient_provider.facility_id)
        outpatient_address = Address.find_by_id(outpatient_facility.address_id)
        outpatient_registration = UserRegister.find_by_id(outpatient_provider_user.registration_id)

        # prescribing provider
        prescirbing_role_id = 2
        pre_patient_provider = PatientsProviders.find_by_patient_and_role_id(patient.id, prescirbing_role_id)
        prescribing_provider = Providers.find_by_id(pre_patient_provider.id)
        prescribing_provider_user = Users.find_by_user_id(prescribing_provider.user_id)
        prescribing_facility = Facilities.find_by_id(prescribing_provider.facility_id)
        prescribing_address = Address.find_by_id(prescribing_facility.address_id)
        prescribing_registration = UserRegister.find_by_id(prescribing_provider_user.registration_id)

        response = {
            "patient": {
                "patient": patient_schema.dump(patient),
                "user": user_schema.dump(user),
                "address": address_schema.dump(address),
                "registration": register_schema.dump(registration)
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
                        "on_call_phone": outpatient_facility.on_call_phone
                    }
                },
                "prescribing": {
                    "registration": register_schema.dump(prescribing_registration),
                    "user": user_schema.dump(prescribing_provider_user),
                    "provider": provider_schema.dump(prescribing_provider),
                    "facility": {
                        "name": prescribing_facility.name,
                        "address": address_schema.dump(prescribing_address),
                        "on_call_phone": prescribing_facility.on_call_phone
                    }
                }
            }
        }

        return jsonify(response)
