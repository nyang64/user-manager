from test.flask_app1 import create_test_app
from test.test_services.populate_data import PopulateData
from unittest import TestCase, mock

import pytest
from db import db
from model.roles import Roles
from model.user_registration import UserRegister
from model.user_status_type import UserStatusType
from model.users import Users
from services.user_services import UserServices
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import InternalServerError, NotFound


class TestUserServices(TestCase):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.user_service = UserServices()
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

    @mock.patch.object(UserRegister, "find_by_email")
    def test_get_detail_by_email_for_none_value(self, mock_user):
        mock_user.return_value = None
        app = create_test_app()
        with app.app_context():
            with pytest.raises(NotFound) as e:
                self.user_service.get_detail_by_email("avilash@gmail.com")
            self.assertIsInstance(e.value, NotFound)
            self.populate_data.create_user("avilash@gmail.com")
            with pytest.raises(NotFound) as e:
                self.user_service.get_detail_by_email("avilash1@gmail.com")
            self.assertIsInstance(e.value, NotFound)

    def test_get_detail_by_email(self):
        app = create_test_app()
        with app.app_context():
            self.populate_data.create_user("avilash@gmail.com")
            resp = self.user_service.get_detail_by_email("avilash@gmail.com")
            self.assertEqual(3, len(resp))

    @mock.patch.object(Users, "check_user_exist")
    def test_delete_user_byid(self, mock_user):
        mock_user.return_value = False
        app = create_test_app()
        with app.app_context():
            with pytest.raises(NotFound) as e:
                self.user_service.delete_user_byid(1)
            self.assertIsInstance(e.value, NotFound)

    @mock.patch.object(UserRegister, "find_by_email")
    def test_get_detail_by_email_raise_exception(self, mock_user):
        # Internal Server Error
        mock_user.side_effect = SQLAlchemyError("Error Raised")
        app = create_test_app()
        with app.app_context():
            with pytest.raises(InternalServerError) as e:
                self.user_service.get_detail_by_email("avilash")
            self.assertIsInstance(e.value, InternalServerError)

    def test_update_user_byid(self):
        app = create_test_app()
        with app.app_context():
            data = self.populate_data.create_user("avilash@gmail.com")
            self.user_service.update_user_byid(data.id, "", "", "")

    @mock.patch.object(Users, "check_user_exist")
    def test_update_user_byid_raises_internal_server_error(self, mock_user):
        mock_user.side_effect = AttributeError("Error Raised")
        app = create_test_app()
        with app.app_context():
            with pytest.raises(InternalServerError) as e:
                self.user_service.update_user_byid(1, "", "", "")
            self.assertIsInstance(e.value, InternalServerError)

    def test_update_user_by_id_raises_not_found(self):
        # Not Found Exception
        app = create_test_app()
        with app.app_context():
            with pytest.raises(NotFound) as e:
                self.user_service.update_user_byid(1, "", "", "")
            self.assertIsInstance(e.value, NotFound)

    @mock.patch.object(UserServices, "assign_role")
    @mock.patch.object(UserServices, "change_user_status")
    def test_register_user(self, mock_user, mock_user_status):
        mock_user.return_value = None
        mock_user_status.return_value = None
        reg = ("email@gmail.com", "password")
        user = ("Avilash", "Jha", "80", "PATIENT", "102-11")
        app = create_test_app()
        with app.app_context():
            UserStatusType(name="ENROLLED").save_to_db()
            Roles(role_name="PATIENT").save_to_db()
            resp = self.user_service.register_user(reg, user)
            self.assertIsInstance(resp, tuple)
            self.assertEqual(len(resp), 2)

    # def test_list_users(self):
    #     app = create_test_app()
    #     with app.app_context():
    #         self.populate_data.create_user("user@gmail.com")
    #         self.populate_data.create_user("user1@gmail.com")
    #         resp = self.user_service.list_users()
    #         self.assertEqual(2, len(resp))

    @mock.patch.object(Users, "find_by_registration_id")
    def test_getUserById_raise_not_found(self, mock_user):
        mock_user.return_value = None
        app = create_test_app()
        with app.app_context():
            with pytest.raises(InternalServerError) as e:
                self.user_service.get_user_by_registration_id(1)
            self.assertIsInstance(e.value, InternalServerError)

    def test_getUserById(self):
        app = create_test_app()
        with app.app_context():
            user = self.populate_data.create_user("user@gmail.com")
            resp = self.user_service.get_user_by_registration_id(user.registration_id)
            self.assertIsNotNone(resp)
