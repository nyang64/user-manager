from test.flask_app1 import create_test_app
from test.test_services.populate_data import PopulateData
from unittest import TestCase, mock

import pytest
from db import db
from model.patients_devices import PatientsDevices
from services.device_manager_api import DeviceManagerApi
from services.patient_services import PatientServices
from services.user_services import UserServices
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import InternalServerError, NotFound, Conflict


class TestPatientServices(TestCase):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.patient_service = PatientServices()
        self.populate_db = PopulateData()

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

    def test_register_patient_raise_indexerror(self):
        app = create_test_app()
        with app.app_context():
            with pytest.raises(IndexError) as e:
                self.patient_service.register_patient((), (), ())
            self.assertIsInstance(e.value, IndexError)
            self.assertIn("out of range", str(e))

    def test_register_patient_raise_typeerror(self):
        app = create_test_app()
        with app.app_context():
            with pytest.raises(TypeError) as e:
                self.patient_service.register_patient(None, None, None)
            self.assertIsInstance(e.value, TypeError)
            self.assertIn("not subscriptable", str(e))

    # def test_save_patient(self):
    #     app = create_test_app()
    #     with app.app_context():
    #         user = self.populate_db.create_user("user@gmail.com")
    #         patient_details = {
    #             "emergency_contact_name": "emer_name",
    #             "emergency_contact_number": "emer_contact",
    #             "date_of_birth": "29/12/1997",
    #             "gender": "male",
    #             "indication": "In",
    #             "address": "",
    #             "user_id": user.id,
    #         }
    #         resp = self.patient_service.save_patient(patient_details)
    #         self.assertIsNotNone(resp)

    @mock.patch.object(PatientServices, "save_patient")
    def test_save_patient_raise_exception(self, save_patient):
        save_patient.side_effect = SQLAlchemyError("Error Sql")
        app = create_test_app()
        patient_details = {
            "emergency_contact_name": "emer_name",
            "emergency_contact_number": "emer_contact",
            "date_of_birth": "29/12/1997",
            "gender": "male",
            "indication": "In",
            "address": "",
            "user_id": 1,
        }

        with app.app_context():
            with pytest.raises(SQLAlchemyError) as e:
                self.patient_service.save_patient(patient_details)
            self.assertIsInstance(e.value, SQLAlchemyError)

    def test_count_device_assigned_raise_exception(self):
        # raise Programing Error Exception
        pass

    @mock.patch.object(
        DeviceManagerApi,
        "get_device",
        return_value={"key": "5678fghijkl", "serial_number": "1212121"},
    )
    @mock.patch.object(DeviceManagerApi, "check_device_exists", return_value=True)
    @mock.patch.object(DeviceManagerApi, "update_device_status", return_value=True)
    @mock.patch.object(PatientsDevices, "device_in_use", return_value=False)
    def test_assign_device_to_patient(
        self, get_device, check_device_exists, update_device_status, mock_device_in_use
    ):
        app = create_test_app()
        with app.app_context():
            patient = self.populate_db.create_patient("patient@gmail.com")
            patient_device = PatientsDevices(
                patient_id=patient.id, device_serial_number="1212121"
            )
            resp = self.patient_service.assign_device_to_patient(patient_device)

            self.assertIsNotNone(resp.id)

    @mock.patch.object(DeviceManagerApi, "check_device_exists", return_value=False)
    @mock.patch.object(PatientsDevices, "device_in_use", return_value=False)
    def test_assign_device_to_patient_raise_exception_not_found(
        self, check_device_exists, mock_device_in_use
    ):
        app = create_test_app()
        with app.app_context():
            with pytest.raises(NotFound) as e:
                patient = self.populate_db.create_patient("patient@gmail.com")
                patient_device = PatientsDevices(
                    patient_id=patient.id, device_serial_number="1212121"
                )

                self.patient_service.assign_device_to_patient(patient_device)
            self.assertIsInstance(e.value, NotFound)


    @mock.patch.object(
        DeviceManagerApi,
        "get_device",
        return_value={"key": "abcde", "serial_number": "88888888"},
    )
    @mock.patch.object(DeviceManagerApi, "get_auth_token", return_value="hello-auth")
    @mock.patch.object(DeviceManagerApi, "check_device_exists", return_value=True)
    @mock.patch.object(DeviceManagerApi, "update_device_status", return_value=True)
    def test_assign_device_to_patient_that_is_already_assigned_raise_exception(
        self, get_device, get_auth_token, check_device_exists, update_device_status
    ):
        app = create_test_app()
        with app.app_context():
            with pytest.raises(Conflict) as e:
                patient = self.populate_db.create_patient("patient@gmail.com")
                patient_device = PatientsDevices(
                    patient_id=patient.id, device_serial_number="88888888"
                )
                patient_device.save_to_db()
                self.patient_service.assign_device_to_patient(patient_device)
            self.assertRaises(Conflict)

    def test_patient_device_list_raise_exception(self):
        pass

    def test_update_patient_data(self):
        app = create_test_app()
        with app.app_context():
            patient = self.populate_db.create_patient("patient@gmail.com")
            self.patient_service.update_patient_data(
                patient.id, "emerc", "ecre", "28/12/1997"
            )

    def test_update_patient_data_raise_exception(self):
        app = create_test_app()
        with app.app_context():
            with pytest.raises(NotFound) as e:
                self.patient_service.update_patient_data(
                    1, "emerc", "ecre", "28/12/1997"
                )
            self.assertIsInstance(e.value, NotFound)

    @mock.patch.object(UserServices, "change_user_status")
    def test_delete_patient_data(self, mock_status):
        app = create_test_app()
        with app.app_context():
            patient = self.populate_db.create_patient("patient@gmail.com")
            self.patient_service.delete_patient_data(patient.id)

    def test_delete_patient_data_raise_exception(self):
        app = create_test_app()
        with app.app_context():
            with pytest.raises(NotFound) as e:
                self.patient_service.delete_patient_data(1)
            self.assertIsInstance(e.value, NotFound)
