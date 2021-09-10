import http
from test.flask_app1 import create_test_app
from unittest import TestCase, mock

import pytest
from model.address import Address
from model.facilities import Facilities
from model.patient import Patient
from model.patients_devices import PatientsDevices
from model.patients_providers import PatientsProviders
from model.providers import Providers
from model.user_registration import UserRegister
from model.users import Users
from resources.patient_manager import PatientManager
from services.patient_services import PatientServices
from werkzeug.exceptions import BadRequest, InternalServerError


def create_patient_req_value():
    return {
        "email": "avilashj34@gmail.com",
        "password": "test12345",
        "first_name": "Preeti",
        "last_name": "Jha",
        "gender": "Female",
        "phone_number": "8097810653",
        "emergency_contact_name": "TL",
        "emergency_contact_number": "7021177481",
        "date_of_birth": "2019-08-08",
        "outpatient_provider": 1,
        "prescribing_provider": 1,
        "indication": "Indic",
        "device_serial_number": "12121212",
    }


class TestPatientManager(TestCase):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.patient = PatientManager()

    @mock.patch.object(PatientServices, "assign_device_to_patient")
    def test_assign_first_device(self, mock_assign):
        mock_assign.return_value = "Test Assigned"
        app = create_test_app()
        with app.test_request_context():
            resp = self.patient.assign_first_device(1, "12121212")
            self.assertEqual("Test Assigned", resp)

    @mock.patch.object(PatientServices, "delete_patient_data")
    @mock.patch("resources.patient_manager.request", spec={})
    def test_delete_patient(self, request, delete_patient_data):
        request.args = {"id": 1}
        expected_resp = ({"message": "Patient deleted"}, http.client.OK)
        app = create_test_app()
        with app.test_request_context():
            resp = PatientManager.delete_patient.__wrapped__(self.patient, "")
            self.assertEqual(resp, expected_resp)

    @mock.patch.object(PatientServices, "delete_patient_data")
    @mock.patch("resources.patient_manager.request", spec={})
    def test_delete_patient_for_non_value(
        self, delete_patient_data, patient_manager_request
    ):
        delete_patient_data.args = {"ida": 1}
        app = create_test_app()
        with app.test_request_context():
            with pytest.raises(BadRequest) as e:
                PatientManager.delete_patient.__wrapped__(self.patient, "")
            self.assertIsInstance(e.value, BadRequest)


    @mock.patch.object(Patient, "find_by_id")
    @mock.patch.object(PatientServices, "update_patient_data")
    @mock.patch("resources.patient_manager.update_patient_schema.load",
                return_value=[None, None, "", ""])
    @mock.patch("resources.patient_manager.request", spec={})
    @mock.patch("utils.validation.request", spec={})
    def test_update_patient(self, mock_req_validation, mock_request, mock_update_schema,
                            mock_patient, update_patient_data):
        mock_req_validation.is_json = True
        mock_req_validation.json = {
            "mobile_app_user": True,
            "device_serial_number": "10000570",
            "indication": "VF",
            "outpatient_provider": "1",
            "external_user_id": "1256",
        }
        mock_request.args = {"id": 1}
        expected_resp = ({"message": "Successfully updated"}, http.client.OK)
        app = create_test_app()
        with app.test_request_context():
            resp = PatientManager.update_patient.__wrapped__(self.patient, "")
            self.assertEqual(resp, expected_resp)

    @mock.patch.object(PatientServices, "update_patient_data")
    @mock.patch("utils.validation.request", spec={})
    @mock.patch("resources.patient_manager.request", spec={})
    def test_update_patient_for_none(self, request, request1, mock_patient):
        request1.is_json = True
        request.args = {"ida": 1}
        app = create_test_app()
        with app.test_request_context():
            with pytest.raises(BadRequest) as e:
                PatientManager.update_patient.__wrapped__(self.patient, "")
            self.assertIsInstance(e.value, BadRequest)

    @mock.patch.object(PatientServices, "assign_device_to_patient")
    @mock.patch("utils.validation.request", spec={})
    def test_assign_device(self, request, mock_patient):
        request.is_json = True
        request.json = {"patient_id": 46, "device_serial_number": "12111214"}
        expeted_resp = (
            {"message": "Device assigned", "status_code": "201"},
            http.client.CREATED,
        )
        app = create_test_app()
        with app.test_request_context():
            resp = PatientManager.assign_device.__wrapped__(self.patient, "")
            self.assertEqual(expeted_resp, resp)

    @mock.patch.object(PatientServices, "patient_device_list")
    def test_patient_device_list(self, mock_patient):
        expected_resp = {"devices": []}
        app = create_test_app()
        mock_patient.return_value = []
        with app.test_request_context():
            resp = PatientManager.patient_device_list.__wrapped__(self.patient, "")
            self.assertEqual(http.client.OK, resp[1])
            self.assertEqual(resp[0].json, expected_resp)

    @mock.patch.object(Address, "find_by_id")
    @mock.patch.object(Facilities, "find_by_id")
    @mock.patch.object(Users, "find_by_id")
    @mock.patch.object(Providers, "find_by_id")
    @mock.patch.object(PatientsProviders, "find_by_patient_and_role_id")
    @mock.patch.object(PatientsDevices, "find_by_patient_id")
    @mock.patch.object(UserRegister, "find_by_id")
    @mock.patch.object(Address, "find_by_user_id")
    @mock.patch.object(Users, "find_by_patient_id")
    @mock.patch.object(Patient, "find_by_id")
    def test_therapy_report_details(
        self,
        mock_patient,
        mock_user,
        mock_address,
        mock_register,
        mock_device,
        mock_patient_provider,
        mock_provider,
        mock_user1,
        mock_facility,
        mock_address1,
    ):
        mock_patient.return_value = Patient(id=1, user_id=1)
        mock_user.return_value = Users(id=1, registration_id=1)
        mock_address.return_value = Address(id=1)
        mock_register.return_value = UserRegister(id=1)
        mock_device.return_value = PatientsDevices(id=1)
        mock_patient_provider.return_value = PatientsProviders(
            id=1, patient_id=1, provider_id=1, provider_role_id=1
        )
        mock_provider.return_value = Providers(id=1, facility_id=1)
        mock_user1.return_value = Users(id=1, registration_id=1)
        mock_facility.return_value = Facilities(id=1, address_id=1)
        mock_address1.return_value = Address(id=1)

        app = create_test_app()
        with app.test_request_context():
            self.patient.therapy_report_details(1)
