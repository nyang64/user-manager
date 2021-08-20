from test.flask_app1 import create_test_app
from test.test_services.populate_data import PopulateData
from unittest import TestCase, mock

import pytest
from db import db
from services.facility_services import FacilityService
from model.facilities import Facilities
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import InternalServerError, NotFound


class TestFacilityServices(TestCase):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.facility_service = FacilityService()
        self.populate_data = PopulateData()
        self.facility_req_json = {
            "address": "123 a st",
            "facility_name": "Kaiser",
            "on_call_phone": "4155555555",
            "external_facility_id": "100-1"
        }
        self.mock_facility = Facilities(
            address_id="1",
            on_call_phone="9090909090", 
            name="facility", 
            external_facility_id="100"
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
        mock_facility_id = 1
        mock_address_id = 2
        app = create_test_app()
        with app.app_context():
            args = self.facility_req_json
            resp1, resp2 = self.facility_service.register_facility(
                args["address"],
                args["facility_name"],
                args["on_call_phone"],
                args["external_facility_id"]
            )
            self.assertIsNotNone(resp1)
            self.assertIsNotNone(resp2)

    def test_list_facilities(self):
        mock_facilities = [self.mock_facility, self.mock_facility]
        mock_address = self.mock_facility
        app = create_test_app()
        with app.test_request_context():
            resp = self.facility_service.list_all_facilities()
            self.assertIsNotNone(resp)
            assert type(resp) == tuple

    @mock.patch.object(Facilities, "find_by_external_id")
    def test_check_facility_exists(self, mock_facility_by_ext_id):
        mock_ext_id = "100-1"
        app = create_test_app()
        with app.test_request_context():
            resp = self.facility_service.check_facility_exists(mock_ext_id)
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

    def test_save_facility(self):
        app = create_test_app()
        with app.app_context():
            address = self.populate_data.create_address()
            resp = self.facility_service.save_facility("F", address.id, "12", "123")
            self.assertIsNotNone(resp)
            self.assertEqual(1, resp)

    @mock.patch.object(FacilityService, "flush_db")
    def test_save_facility_raise_exception(self, mock_flush):
        mock_flush.return_value = None
        app = create_test_app()
        with app.app_context():
            with pytest.raises(InternalServerError) as e:
                self.facility_service.save_facility("F", 1, "12", "1234567")
            self.assertIsInstance(e.value, InternalServerError)
