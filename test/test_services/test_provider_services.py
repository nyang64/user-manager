from test.flask_app1 import create_test_app
from test.test_services.populate_data import PopulateData
from unittest import TestCase, mock

import pytest
from db import db
from model.facilities import Facilities
from model.provider_role_types import ProviderRoleTypes
from services.provider_services import ProviderService
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import InternalServerError, NotFound


class TestProviderServices(TestCase):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.provider_service = ProviderService()
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

    def test_base_query(self):
        app = create_test_app()
        with app.app_context():
            resp = self.provider_service._base_query(1)
            self.assertIsNotNone(resp)

    def test_filter_query_raise_not_found(self):
        app = create_test_app()
        with app.app_context():
            base = self.provider_service._base_query(1)
            with pytest.raises(NotFound) as e:
                self.provider_service._filter_query(base, "A", "J", "20/12", 1)
            self.assertIsInstance(e.value, NotFound)

    def test_filter_query(self):
        app = create_test_app()
        with app.app_context():
            base = self.provider_service._base_query(1)
            resp = self.provider_service._filter_query(base, "A", "J", "20/12", None)
            self.assertIsNotNone(resp)
            therapy = self.populate_data.create_therapy_report()
            resp1 = self.provider_service._filter_query(
                base, "A", "J", "20/12", therapy.id
            )
            self.assertIsNotNone(resp1)

    @mock.patch.object(ProviderRoleTypes, "find_by_name")
    def test_add_provider(self, mock_provider_role):
        mock_provider_role.return_value = ProviderRoleTypes(id=1)
        app = create_test_app()
        with app.app_context():
            user = self.populate_data.create_user("user@gmail.com")
            fac = self.populate_data.create_facility()
            self.populate_data.provider_role_types()
            resp = self.provider_service.add_provider(user.id, fac.id, "prescribing")
            self.assertIsNotNone(resp)
            self.assertEqual(1, resp)

    def test_add_provider_raise_not_found_1(self):
        app = create_test_app()
        with app.app_context():
            user = self.populate_data.create_user("user@gmail.com")
            fac = self.populate_data.create_facility()
            with pytest.raises(NotFound) as e:
                self.provider_service.add_provider(user.id, fac.id, "outpat")
            self.assertIsInstance(e.value, NotFound)

    @mock.patch.object(Facilities, "find_by_id")
    def test_add_provider_raise_not_found(self, mock_facility):
        mock_facility.return_value = False
        app = create_test_app()
        with app.app_context():
            with pytest.raises(NotFound) as e:
                self.provider_service.add_provider(1, 1, "")
            self.assertIsInstance(e.value, NotFound)

    def test_report_signed_link_for_none(self):
        app = create_test_app()
        with app.app_context():
            resp = self.provider_service.report_signed_link(1)
            self.assertTupleEqual(resp, ("No report found", 404))

    @mock.patch("utils.common.generate_signed_url")
    def test_report_signed_link(self, mock_link):
        mock_link.return_value = "KEY"
        app = create_test_app()
        with app.app_context():
            salvos = self.populate_data.create_salvos_report()
            resp = self.provider_service.report_signed_link(salvos.id)
            self.assertTupleEqual(resp, ("KEY", 200))

    def test_update_uploaded_ts(self):
        app = create_test_app()
        with app.app_context():
            resp = self.provider_service.update_uploaded_ts(None)
            self.assertIsNotNone(resp)
            self.assertTupleEqual(resp, ("reportId is None", 404))
            resp1 = self.provider_service.update_uploaded_ts(1)
            self.assertIsNotNone(resp1)
            self.assertTupleEqual(resp1, ("not found", 404))
            salvos = self.populate_data.create_salvos_report()
            resp2 = self.provider_service.update_uploaded_ts(salvos.therapy_report_id)
            self.assertIsNotNone(resp2)
            self.assertTupleEqual(resp2, ("updated data", 201))

    def test_patients_list_raise_not_found(self):
        from db import db

        app = create_test_app()
        with app.app_context():
            with pytest.raises(NotFound) as e:
                self.provider_service.patients_list(1, 1, 10, "A", "J", "29/12", None)
            self.assertIsInstance(e.value, NotFound)

    def test_patient_detail_byid(self):
        app = create_test_app()
        with app.app_context():
            resp = self.provider_service.patient_detail_byid(1)
            self.assertTupleEqual(resp, ({}, []))

    @mock.patch.object(ProviderService, "add_provider")
    # @mock.patch.object(UserServices, 'assign_role')
    # @mock.patch.object(UserServices, 'save_user')
    # @mock.patch.object(AuthServices, 'register_new_user')
    def test_register_provider(self, mock_provider):
        # mock_register.return_value = 1
        # mock_user.return_value = 1, '121wd'
        # mock_role.return_value = None
        mock_provider.return_value = 2
        app = create_test_app()
        reg = ("avi@gmail.com", "avi")
        user = ("F", "L", "121212")
        with app.app_context():
            self.populate_data.add_roles()
            resp = self.provider_service.register_provider_service(
                reg, user, 1, "PROVIDER"
            )
            self.assertIsNotNone(resp)
            self.assertEqual(2, resp)
        mock_provider.side_effect = SQLAlchemyError("Error Occured")
        with app.app_context():
            with pytest.raises(InternalServerError) as e:
                self.provider_service.register_provider_service(
                    reg, user, 1, "PROVIDER"
                )
            self.assertIsInstance(e.value, InternalServerError)
