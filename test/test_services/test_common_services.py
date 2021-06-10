from test.flask_app1 import create_test_app
from test.test_services.populate_data import PopulateData
from unittest import TestCase, mock

import pytest
from db import db
from model.patient import Patient
from model.user_registration import UserRegister
from services.common_services import CommonRepo
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import Conflict, InternalServerError, NotFound


class TestCommonServices(TestCase):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.common_service = CommonRepo()
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

    def test_check_patient_exists_raise_not_found(self):
        app = create_test_app()
        with app.app_context():
            with pytest.raises(NotFound) as e:
                self.common_service.check_patient_exist(1)
            self.assertIsInstance(e.value, NotFound)

    def test_check_patient_exists(self):
        app = create_test_app()
        with app.app_context():
            self.populate_data.create_patient("patient@gmail.com")
            resp = self.common_service.check_patient_exist(1)
            self.assertIsInstance(resp, Patient)

    def test_is_email_registered_raise_conflict(self):
        app = create_test_app()
        with app.app_context():
            self.populate_data.register_user("e@gmail.com")
            with pytest.raises(Conflict) as e:
                self.common_service.is_email_registered("e@gmail.com")
            self.assertIsInstance(e.value, Conflict)

    @mock.patch.object(UserRegister, "find_by_email")
    def test_is_email_registered_raise_internal_error(self, mock_reg):
        mock_reg.side_effect = SQLAlchemyError("Error")
        app = create_test_app()
        with app.app_context():
            self.populate_data.register_user("e@gmail.com")
            with pytest.raises(InternalServerError) as e:
                self.common_service.is_email_registered("e@gmail.com")
            self.assertIsInstance(e.value, InternalServerError)

    def test_is_email_registered(self):
        app = create_test_app()
        with app.app_context():
            self.populate_data.register_user("e@gmail.com")
            resp = self.common_service.is_email_registered("e1@gmail.com")
            self.assertIsNone(resp)
