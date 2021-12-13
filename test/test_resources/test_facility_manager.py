import http
from test.flask_app1 import create_test_app
from unittest import TestCase, mock

import pytest
from model.facilities import Facilities
from resources.facilities_manager import FacilitiesManager
from services.facility_services import FacilityService
from werkzeug.exceptions import BadRequest

def create_facility_req_value():
    return {
        "facility_name":"Kaiser",
        "on_call_phone": "4155555555",
        "external_facility_id": "100-1",
    }

class TestProviderManager(TestCase):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.facility = FacilitiesManager()


    @mock.patch.object(FacilityService, "check_facility_exists_by_external_id")
    @mock.patch("utils.validation.request", spec={})
    def test_add_facility(self, mock_req, mock_facility):
        mock_req.is_json = True
        mock_req.json = create_facility_req_value()
        mock_facility.return_value = True
        app = create_test_app()
        with app.test_request_context():
            resp = self.facility.add_facility.__wrapped__(self.facility, {"user_email": "123@mail.com", "user_role": "ADMIN"})
            self.assertIsNotNone(resp)
            assert type(resp) == tuple

    @mock.patch.object(FacilityService, "check_facility_exists_by_external_id")
    def test_add_facility_none(self, mock_facility):
        mock_facility.return_value = None
        app = create_test_app()
        with app.test_request_context():
            with pytest.raises(BadRequest) as e:
                resp = self.facility.add_facility.__wrapped__(self.facility, {"user_email": "123@mail.com", "user_role": "ADMIN"})
            assert type(e.value) is BadRequest

    @mock.patch("model.facilities.Facilities.all")
    def test_list_facilities(self, mock_facility):
        mock_facility = Facilities(address_id="1", on_call_phone="9090909090", name="facility", external_facility_id="100")
        app = create_test_app()
        with app.test_request_context():
            resp = self.facility.get_facilities_list.__wrapped__(self.facility, {"user_email": "esadmin@elementsci.com", "user_role": "ADMIN"})
            self.assertIsNotNone(resp)
            assert type(resp) == tuple