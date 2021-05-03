import http
from test.flask_app1 import create_test_app
from unittest import TestCase, mock

import pytest
from resources.provider_manager import ProviderManager
from services.facility_services import FacilityService
from services.provider_services import ProviderService
from services.user_services import UserServices
from werkzeug.exceptions import BadRequest


class TestProviderManager(TestCase):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.provider = ProviderManager()

    @mock.patch.object(ProviderService, "patient_detail_byid")
    @mock.patch("resources.provider_manager.request", spec={})
    def test_get_patient_detail_byid(self, request, mock_patient):
        request.args = {"patientID": 1}
        app = create_test_app()
        mock_patient.return_value = None, None
        with app.test_request_context():
            resp = ProviderManager.get_patient_detail_byid.__wrapped__(
                self.provider, ""
            )
            print(resp[0].json)
            self.assertEqual(resp[0].json, {"report": {}})
            self.assertEqual(resp[1], http.client.OK)

    @mock.patch.object(ProviderService, "report_signed_link")
    @mock.patch("resources.provider_manager.request", spec={})
    def test_get_report_signed_link(self, request, mock_patient):
        request.args = {"reportId": 1}
        app = create_test_app()
        mock_patient.return_value = "signed", http.client.OK
        with app.test_request_context():
            resp = ProviderManager.get_report_signed_link.__wrapped__(self.provider, "")
            self.assertEqual(resp[0], {"report_url": "signed"})
            self.assertEqual(resp[1], http.client.OK)

    @mock.patch.object(ProviderService, "update_uploaded_ts")
    @mock.patch("utils.validation.request", spec={})
    def test_update_uploaded_ts(self, request, mock_patient):
        request.is_json = True
        request.json = {"reportId": 1}
        app = create_test_app()
        mock_patient.return_value = "signed", http.client.OK
        with app.test_request_context():
            resp = ProviderManager.update_uploaded_ts.__wrapped__(self.provider, "")
            self.assertEqual(
                resp[0], {"message": "signed", "status_code": http.client.OK}
            )
            self.assertEqual(resp[1], http.client.OK)

    @mock.patch.object(FacilityService, "register_facility")
    @mock.patch("utils.validation.request", spec={})
    def test_add_facility(self, request, mock_patient):
        request.is_json = True
        request.json = {
            "facility_name": "FCAJ",
            "on_call_phone": "3122318112",
            "address": {
                "street_address_1": "Test",
                "street_address_2": "Te",
                "city": "Kyn",
                "state": "MH",
                "country": "IN",
                "postal_code": "421306",
            },
        }
        app = create_test_app()
        mock_patient.return_value = 1, 2
        expected = {
            "address_id": 1,
            "facility_id": 2,
            "status_code": http.client.CREATED,
        }
        with app.test_request_context():
            resp = ProviderManager.add_facility.__wrapped__(self.provider, "")
            self.assertEqual(resp[0], expected)
            self.assertEqual(resp[1], http.client.CREATED)
