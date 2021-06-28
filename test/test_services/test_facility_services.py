from test.flask_app1 import create_test_app
from test.test_services.populate_data import PopulateData
from unittest import TestCase, mock

import pytest
from db import db
from services.facility_services import FacilityService
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import InternalServerError, NotFound


class TestFacilityServices(TestCase):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.facility_service = FacilityService()
        self.populate_data = PopulateData()

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
            resp = self.facility_service.save_facility("F", address.id, "12")
            self.assertIsNotNone(resp)
            self.assertEqual(1, resp)

    @mock.patch.object(FacilityService, "flush_db")
    def test_save_facility_raise_exception(self, mock_flush):
        mock_flush.return_value = None
        app = create_test_app()
        with app.app_context():
            with pytest.raises(InternalServerError) as e:
                self.facility_service.save_facility("F", 1, "12")
            self.assertIsInstance(e.value, InternalServerError)
