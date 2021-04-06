from resources.patient_manager import PatientManager
from services.patient_services import PatientServices
from test.flask_app1 import create_test_app
from werkzeug.exceptions import BadRequest
from unittest import TestCase
from unittest import mock
import pytest
import http


class TestPatientManager(TestCase):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.patient = PatientManager()

    @mock.patch.object(PatientServices, 'delete_patient_data')
    @mock.patch('resources.patient_manager.request', spec={})
    def test_delete_patient(self, request, mock_patient):
        request.args = {"id": 1}
        expected_resp = ({'message': 'Patient deleted'},
                         http.client.OK)
        app = create_test_app()
        with app.test_request_context():
            resp = PatientManager.delete_patient.__wrapped__(self.patient, '')
            self.assertEqual(resp, expected_resp)

    @mock.patch.object(PatientServices, 'delete_patient_data')
    @mock.patch('resources.patient_manager.request', spec={})
    def test_delete_patient_for_non_value(self, request, mock_patient):
        request.args = {"ida": 1}
        app = create_test_app()
        with app.test_request_context():
            with pytest.raises(BadRequest) as e:
                PatientManager.delete_patient.__wrapped__(self.patient, '')
            self.assertIsInstance(e.value, BadRequest)

    @mock.patch.object(PatientServices, 'update_patient_data')
    @mock.patch('utils.validation.request', spec={})
    @mock.patch('resources.patient_manager.request', spec={})
    def test_update_patient(self, request, request1, mock_patient):
        request1.is_json = True
        request.args = {"id": 1}
        request1.json = {
            "emergency_contact_name": "avilash",
            "emergency_contact_number": "1212121212",
            "date_of_birth": "2019-08-08"
        }
        expected_resp = ({'message': 'Sucessfully updated'},
                         http.client.OK)
        app = create_test_app()
        with app.test_request_context():
            resp = PatientManager.update_patient.__wrapped__(self.patient, '')
            self.assertEqual(resp, expected_resp)

    @mock.patch.object(PatientServices, 'update_patient_data')
    @mock.patch('utils.validation.request', spec={})
    @mock.patch('resources.patient_manager.request', spec={})
    def test_update_patient_for_none(self, request, request1, mock_patient):
        request1.is_json = True
        request.args = {"ida": 1}
        app = create_test_app()
        with app.test_request_context():
            with pytest.raises(BadRequest) as e:
                PatientManager.update_patient.__wrapped__(self.patient, '')
            self.assertIsInstance(e.value, BadRequest)

    @mock.patch.object(PatientServices, 'assign_device_to_patient')
    @mock.patch('utils.validation.request', spec={})
    def test_assign_device(self, request, mock_patient):
        request.is_json = True
        request.json = {
            "patient_id": 46,
            "device_serial_number": "12111214"
        }
        expeted_resp = ({'message': 'Device assigned',
                        'status_code': '201'}, http.client.CREATED)
        app = create_test_app()
        with app.test_request_context():
            resp = PatientManager.assign_device.__wrapped__(self.patient, '')
            self.assertEqual(expeted_resp, resp)

    @mock.patch.object(PatientServices, 'patient_device_list')
    def test_patient_device_list(self, mock_patient):
        expected_resp = {'devices': []}
        app = create_test_app()
        mock_patient.return_value = []
        with app.test_request_context():
            resp = PatientManager.patient_device_list.__wrapped__(
                self.patient, '')
            self.assertEqual(http.client.OK, resp[1])
            self.assertEqual(resp[0].json, expected_resp)
