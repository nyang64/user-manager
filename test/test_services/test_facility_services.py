from test.flask_app1 import create_test_app
from test.test_services.populate_data import PopulateData
from unittest import TestCase, mock

import pytest
from db import db
from services.facility_services import FacilityService
from model.facilities import Facilities
from model.address import Address
from werkzeug.exceptions import InternalServerError, NotFound
from sqlalchemy import exc


mock_facility_data = Facilities(
            address_id="1",
            on_call_phone="9090909090",
            name="facility",
            external_facility_id="100"
        )

def get_facilities():
    f = Facilities(
            address_id="1",
            on_call_phone="9090909090",
            name="facility",
            external_facility_id="100"
        )
    list_f = [f, f]
    return list_f

def get_address():
    address = Address()
    address.street_address_2 = "test"
    address.street_address_1 = "123 Address st"
    address.city = "fresno"
    address.state = "IL"
    address.country = "US"
    address.postal_code = "12345"
    return address

class TestFacilityServices(TestCase):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.facility_service = FacilityService()
        self.populate_data = PopulateData()
        self.facility_req_json = {
            "address": "123 a st",
            "facility_name": "Kaiser",
            "on_call_phone": "4155555555",
            "external_facility_id": "100-1",
            "primary_contact_id": 1
        }
        self.mock_facility = Facilities(
            address_id="1",
            on_call_phone="9090909090",
            name="facility",
            external_facility_id="100",
            primary_contact_id=1
        )

    def setUp(self):
        """Setting Up Database"""
        app = create_test_app()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Dropping all the database"""
        app = create_test_app()
        with app.app_context():
            db.session.remove()
            db.drop_all()

    @mock.patch.object(FacilityService, "save_facility")
    @mock.patch.object(FacilityService, "save_address")
    def test_register_facility(self, mock_facility_id, mock_address_id):
        app = create_test_app()
        with app.app_context():
            args = self.facility_req_json
            resp1, resp2 = self.facility_service.register_facility(
                args["address"],
                args["facility_name"],
                args["on_call_phone"],
                args["external_facility_id"],
                args["primary_contact_id"]
            )
            self.assertIsNotNone(resp1)
            self.assertIsNotNone(resp2)

    @mock.patch("services.facility_services.Facilities.all", return_value=get_facilities())
    @mock.patch("services.facility_services.Address.find_by_id", return_value=get_address())
    def test_list_facilities_with_facilities_data(self, mock_facility, mock_address):
        app = create_test_app()
        with app.test_request_context():
            resp, count = self.facility_service.list_all_facilities()
            self.assertIsNotNone(resp)
            assert len(resp) == 2

    @mock.patch("services.facility_services.Facilities.all", return_value=[])
    def test_list_facilities_with_no_data(self, mock_facility):
        app = create_test_app()
        with app.test_request_context():
            resp, count = self.facility_service.list_all_facilities()
            self.assertIsNotNone(resp)
            assert len(resp) == 0

    @mock.patch("services.facility_services.Facilities.all", return_value=[])
    def test_list_facilities_with_exception(self, mock_facility):
        mock_facility.side_effect = exc.SQLAlchemyError
        app = create_test_app()
        with app.test_request_context():
            with pytest.raises(InternalServerError) as e:
                resp, count = self.facility_service.list_all_facilities()
                assert True

    @mock.patch("services.facility_services.Facilities.find_by_id", return_value=mock_facility_data)
    def test_get_facility_by_id_with_noexception(self, mock_facility):
        app = create_test_app()
        with app.test_request_context():
            facility = self.facility_service.get_facility_by_id(2)
            assert facility is not None

    @mock.patch("services.facility_services.Facilities.find_by_id")
    def test_get_facility_by_id_with_exception(self, mock_facility):
        mock_facility.side_effect = Exception ("error")
        app = create_test_app()
        with app.test_request_context():
            with pytest.raises(Exception) as e:
                facility = self.facility_service.get_facility_by_id(2)
                assert True


    @mock.patch.object(Facilities, "find_by_external_id")
    def test_check_facility_exists(self, mock_facility_by_ext_id):
        mock_ext_id = "100-1"
        app = create_test_app()
        with app.test_request_context():
            resp = self.facility_service.check_facility_exists_by_external_id(mock_ext_id)
            self.assertIsNotNone(resp)
            assert type(resp) == bool
            self.assertEqual(resp, True)

    def test_save_address(self):
        app = create_test_app()
        with app.app_context():
            args = self.populate_data.create_address()
            resp = self.facility_service.save_address(args)
            self.assertIsNotNone(resp)
            self.assertEqual(1, resp)

    def test_save_address_exception(self):
        app = create_test_app()
        with app.app_context():
            with pytest.raises(InternalServerError) as e:
                self.facility_service.save_address(None)
            self.assertIsInstance(e.value, InternalServerError)

    @mock.patch.object(FacilityService, "flush_db")
    def test_save_facility_raise_exception(self, mock_flush):
        mock_flush.return_value = None
        app = create_test_app()
        with app.app_context():
            with pytest.raises(InternalServerError) as e:
                self.facility_service.save_facility("F", 1, "12", "1234567", 1)
            self.assertIsInstance(e.value, InternalServerError)

    @mock.patch.object(FacilityService, "_FacilityService__update_facility_data")
    @mock.patch.object(Facilities, "find_by_id")
    @mock.patch.object(Address, "find_by_id")
    @mock.patch.object(FacilityService, "commit_db")
    def test_update_facility_no_address(self, mock_commit, mock_add_id, mock_fac_id, mock_update):
        app = create_test_app()
        with app.app_context():
            with pytest.raises(InternalServerError) as e:
                self.facility_service.update_facility(1, None,
                                     "test", "1232311234", "100", 1)
            self.assertIsInstance(e.value, InternalServerError)
