import http
from test.flask_app1 import create_test_app
from unittest import TestCase, mock

import pytest
from model.address import Address
from model.facilities import Facilities
from model.providers import Providers
from model.providers_roles import ProviderRoles
from model.user_registration import UserRegister
from model.users import Users
from resources.provider_manager import ProviderManager
from services.facility_services import FacilityService
from services.provider_services import ProviderService
from werkzeug.exceptions import BadRequest


def create_provider_req_value():
    return {
        "first_name": "Laura",
        "last_name": "Kirby",
        "facility_id": "1",
        "phone_number": "9988776111",
        "email": "laura@elementsci.com",
        "role": "outpatient",
        "external_user_id": "101-103"
    }

def create_facility_req_value():
    return {
        "facility_name":"Kaiser",
        "on_call_phone": "4155555555",
        "external_facility_id": "100-1",
    }


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

            # self.assertEqual(resp[0].json, {"report": {}})
            #     self.provider, '')
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

    @mock.patch("utils.validation.request", spec={})
    def test_register_provider_incorect_param(self, mock_req):
        mock_req.return_value = {}
        app = create_test_app()
        with app.test_request_context():
            with pytest.raises(BadRequest) as e:
                self.provider.register_provider.__wrapped__(self.provider, "")
            self.assertIsInstance(e.value, BadRequest)

    @mock.patch.object(UserRegister, "find_by_id")
    @mock.patch.object(Users, "find_by_id")
    @mock.patch.object(ProviderRoles, "find_by_provider_id")
    @mock.patch.object(Address, "find_by_id")
    @mock.patch.object(Facilities, "find_by_id")
    @mock.patch.object(Providers, "find_by_id")
    @mock.patch.object(ProviderService, "register_provider_service")
    @mock.patch("resources.provider_manager.send_provider_registration_email")
    @mock.patch("resources.provider_manager.request", spec={})
    def test_register_provider(
        self,
        mock_req,
        mock_email,
        mock_service,
        mock_provider,
        mock_facility,
        mock_address,
        mock_prole,
        mock_user,
        mock_register
    ):
        mock_req.json = create_provider_req_value()
        mock_service.return_value = 1
        mock_provider.return_value = Providers(id=1, user_id=1)
        mock_facility.return_value = Facilities(id=1, address_id=1)
        mock_address.return_value = Address(id=1)
        mock_prole.return_value = [ProviderRoles(id=1)]
        mock_user.return_value = Users(id=1, registration_id=1)
        mock_register.return_value = UserRegister(id=1)
        app = create_test_app()
        with app.test_request_context():
            resp = self.provider.register_provider.__wrapped__(self.provider, {"user_email": "123@mail.com", "user_role": "ADMIN"})
            self.assertIsNotNone(resp)
            self.assertEqual(2, len(resp))
            self.assertEqual(resp[1], 201)

    @mock.patch.object(Providers, "find_providers")
    def test_get_providers_for_none(self, mock_provider):
        mock_provider.return_value = None
        app = create_test_app()
        with app.test_request_context():
            resp = self.provider.get_providers.__wrapped__(self.provider, "")
            self.assertIsNotNone(resp)
            self.assertEqual(2, len(resp))
            self.assertTupleEqual(resp, ({"message": "No Providers Found"}, 404))

    @mock.patch.object(Providers, "find_providers")
    @mock.patch.object(Users, "find_by_id")
    @mock.patch.object(Facilities, "find_by_id")
    @mock.patch.object(ProviderService, "list_all_patients_by_provider")
    def test_get_providers(self, mock_provider, mock_users, mock_facilities, mock_provider_service):
        mock_provider.return_value = [Providers(user_id=1, facility_id=1), Providers(user_id=1, facility_id=1)]
        mock_users.return_value = Users(registration_id=1, first_name="John", last_name="Doe", phone_number="4155555555", uuid="13212314324")
        mock_facilities.return_value = Facilities(address_id=1, name="Kaiser", external_facility_id="100", on_call_phone="4155555555")
        mock_provider_service.return_valie = []
        app = create_test_app()
        with app.test_request_context():
            resp = self.provider.get_providers.__wrapped__(self.provider, "")
            self.assertIsNotNone(resp)
            self.assertEqual(2, len(resp))
            self.assertTupleEqual(
                resp,
                (
                    {
                        "message": "Users Found",
                        "data": [],
                    },
                    200,
                ),
            )
            # self.assertTupleEqual(
            #     resp,
            #     (
            #         {
            #             "message": "Users Found",
            #             "data": [{
            #                 "id": 1,
            #                 "user_id": 1,
            #                 "facility_id": 1,
            #                 "first_name": "John",
            #                 "last_name": "Doe",
            #                 "phone_number": "4155555555",
            #                 "facility_name": "Kaiser",
            #                 "patients": [],
            #             }],
            #         },
            #         200,
            #     ),
            # )

    @mock.patch.object(FacilityService, "check_facility_exists")
    @mock.patch("utils.validation.request", spec={})
    def test_add_facility(self, mock_req, mock_facility):
        mock_req.is_json = True
        mock_req.json = create_facility_req_value()
        mock_facility.return_value = True
        app = create_test_app()
        with app.test_request_context():
            resp = self.provider.add_facility.__wrapped__(self.provider, {"user_email": "123@mail.com", "user_role": "ADMIN"})
            self.assertIsNotNone(resp)
            assert type(resp) == tuple

    @mock.patch.object(FacilityService, "check_facility_exists")
    def test_add_facility_none(self, mock_facility):
        mock_facility.return_value = None
        app = create_test_app()
        with app.test_request_context():
            with pytest.raises(BadRequest) as e:
                resp = self.provider.add_facility.__wrapped__(self.provider, "")
            assert type(e.value) is BadRequest

    @mock.patch("model.facilities.Facilities.all")
    def test_list_facilities(self, mock_facility):
        mock_facility = Facilities(address_id="1", on_call_phone="9090909090", name="facility", external_facility_id="100")
        app = create_test_app()
        with app.test_request_context():
            resp = self.provider.get_facilities_list.__wrapped__(self.provider, {"user_email": "esadmin@elementsci.com", "user_role": "ADMIN"})
            self.assertIsNotNone(resp)
            assert type(resp) == tuple
