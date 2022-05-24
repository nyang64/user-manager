from test.flask_app1 import create_test_app
from test.test_services.populate_data import PopulateData
from unittest import TestCase, mock
from unittest.mock import MagicMock

import pytest
from db import db
from model.address import Address
from model.patients_devices import PatientsDevices
from model.provider_role_types import ProviderRoleTypes
from model.user_registration import UserRegister
from model.users import Users
from model.patient import Patient
from model.patients_providers import PatientsProviders
from model.patients_patches import PatientsPatches
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

    @mock.patch.object(UserServices, "register_user", return_value=[2, "1223333232asas"])
    @mock.patch("services.patient_services.PatientServices.enroll_newsletter")
    @mock.patch("services.patient_services.PatientServices.assign_providers")
    @mock.patch("services.patient_services.PatientServices.save_address", return_value="1")
    @mock.patch("services.patient_services.PatientServices.save_patient", return_value="5")
    @mock.patch("services.patient_services.PatientServices._save_patient_details")
    def test_register_patient_success(self, mock_details, mock_pat, mock_addr, mock_prov, mock_enroll, mock_user_svc):
        register = UserRegister(email="123@es.com")
        user = Users(first_name="123")
        patient_details = {
            "patient": {
                           "shipping_address": {
                               "street_address_1": "121212",
                               "street_address_2": "1111"
                           },
                           "permanent_address": {
                               "street_address_1": "test steee",
                               "street_address_2": "1234"
                           }
                    },
            "providers": {
                "outpatient_provider_id": 5,
                "prescribing_provider_id": 3
            },
            "details": {
                "shoulder_strap_back": "14124",
                "shoulder_strap_front": "124124",
                "starter_kit_lot_number": "123456789",
                "upper_patch_setting": "124",
                "enrollment_notes": "Test",
                "mobile_model": "",
                "mobile_os_version": "",
                "other_phone": "",
                "pa_setting_back": "",
                "pa_setting_front": ""
            }
        }
        app = create_test_app()
        with app.app_context():
            patient_id = self.patient_service.register_patient(register, user, patient_details)
            self.assertIsNotNone(patient_id)

    @mock.patch.object(UserServices, "register_user", return_value=[2, "1223333232asas"])
    @mock.patch("services.patient_services.PatientServices.enroll_newsletter")
    @mock.patch("services.patient_services.PatientServices.assign_providers")
    @mock.patch("services.patient_services.PatientServices.save_address", return_value="1")
    @mock.patch("services.patient_services.PatientServices.save_patient", return_value="5")
    @mock.patch("services.patient_services.PatientServices._save_patient_details")
    def test_register_patient_success_no_shipping_key(self, mock_det, mock_pat, mock_addr, mock_prov, mock_enroll, mock_user_svc):
        register = UserRegister(email="123@es.com")
        user = Users(first_name="123")
        patient_details = {
            "patient": {
                "permanent_address": {
                    "street_address_1": "test steee",
                    "street_address_2": "1234"
                }
            },
            "providers": {
                "outpatient_provider_id": 5,
                "prescribing_provider_id": 3
            },
            "details": {
                "shoulder_strap_back": "1212121"
            }
        }
        app = create_test_app()
        with app.app_context():
            patient_id = self.patient_service.register_patient(register, user, patient_details)
            self.assertIsNotNone(patient_id)

    @mock.patch.object(UserServices, "register_user", return_value=[2, "1223333232asas"])
    @mock.patch("services.patient_services.PatientServices.enroll_newsletter")
    @mock.patch("services.patient_services.PatientServices.assign_providers")
    @mock.patch("services.patient_services.PatientServices.save_address", return_value="1")
    @mock.patch("services.patient_services.PatientServices.save_patient", return_value="5")
    @mock.patch("services.patient_services.PatientServices._save_patient_details")
    def test_register_patient_success_with_shipping_key(self, mock_det, mock_pat, mock_addr, mock_prov, mock_enroll, mock_user_svc):
        register = UserRegister(email="123@es.com")
        user = Users(first_name="123")
        patient_details = {
            "patient": {
                "permanent_address": {
                    "street_address_1": "test steee",
                    "street_address_2": "1234"
                },
                "shipping_address": {

                }
            },
            "providers": {
                "outpatient_provider_id": 5,
                "prescribing_provider_id": 3
            },
            "details": {
                "shoulder_strap_back": "1212121"
            }
        }
        app = create_test_app()
        with app.app_context():
            patient_id = self.patient_service.register_patient(register, user, patient_details)
            self.assertIsNotNone(patient_id)

    @mock.patch("services.patient_services.PatientServices.flush_db")
    @mock.patch("services.patient_services.PatientServices.commit_db")
    def test_enroll_newsletter(self, commit, flush):
        app = create_test_app()
        with app.app_context():
            self.patient_service.enroll_newsletter(1)

    @mock.patch.object(ProviderRoleTypes, "find_by_name")
    @mock.patch("services.patient_services.PatientServices.flush_db")
    @mock.patch("services.patient_services.PatientServices.commit_db")
    def test_assign_providers(self, commit, flush, provider_role):
        app = create_test_app()
        with app.app_context():
            self.patient_service.assign_providers(patient_id=1, outpatient_provider_id=2,
                                                  prescribing_provider_id=3)

    @mock.patch.object(Users, "check_user_exist")
    @mock.patch("services.patient_services.PatientServices.flush_db")
    @mock.patch("services.patient_services.PatientServices.commit_db")
    def test_save_patient(self, commit, flush, users):
        app = create_test_app()
        with app.app_context():
            self.patient_service.save_patient({"user_id": "1"})

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

    @mock.patch.object(PatientServices, "save_patient")
    @mock.patch("services.patient_services.PatientServices.flush_db")
    @mock.patch("services.patient_services.PatientServices.commit_db")
    def test_save_patient_details(self, commit, flush, save_patient):
        app = create_test_app()
        patient_details = {
            "patient_id": "1",
            "pa_setting_front": "0.4"
        }

        with app.app_context():
            self.patient_service._save_patient_details(1, patient_details)
            # verify that flush and commit were invoked
            flush.assert_called_once()
            commit.assert_called_once()

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

    def test_remove_patient_device_association_with_no_devices(self):
        app = create_test_app()
        with app.app_context():
            value = self.patient_service.remove_patient_device_association("123456")
            self.assertEqual(value, None)

    @mock.patch.object(PatientsDevices, "find_by_device_serial_number",
                       return_value=PatientsDevices(patient_id=1, device_serial_number="1234567"))
    @mock.patch("services.patient_services.PatientServices.flush_db")
    @mock.patch("services.patient_services.PatientServices.commit_db")
    @mock.patch.object(DeviceManagerApi, "check_device_exists", return_value=True)
    @mock.patch.object(DeviceManagerApi, "update_device_status", return_value=True)
    def test_remove_patient_device_association_with_devices(self, commit, flush, pat_dev, mock_check_device, mock_update_status):
        app = create_test_app()
        with app.app_context():
            self.patient_service.remove_patient_device_association("123456")

    @mock.patch.object(UserServices, "change_user_status")
    def test_delete_patient_data(self, mock_status):
        app = create_test_app()
        with app.app_context():
            patient = self.populate_db.create_patient("patient@gmail.com")
            self.patient_service.delete_patient_data(patient.id, "", "")

    def test_delete_patient_data_raise_exception(self):
        app = create_test_app()
        with app.app_context():
            with pytest.raises(NotFound) as e:
                self.patient_service.delete_patient_data(1, "", "")
            self.assertIsInstance(e.value, NotFound)

    @mock.patch.object(Users, "find_by_id", return_value=None)
    def test_update_patient_data_raises_no_user_error(self, users):
        patient = Patient(user_id=1)
        app = create_test_app()
        with app.app_context():
            with pytest.raises(InternalServerError) as e:
                self.patient_service.update_patient_data(None, "test", patient, None, patient)

    @mock.patch.object(Users, "find_by_id")
    @mock.patch.object(UserRegister, "find_by_id", return_value=None)
    @mock.patch("services.patient_services.db.session")
    def test_update_patient_data_raises_no_registration(self, mock_session, mock_users, mock_register):
        user_from_db = Users(first_name="Test",
                             last_name="Name",
                             phone_number="2312311231",
                             external_user_id="123")

        user_from_req = Users(first_name="Test_2",
                              last_name="Name_2",
                              phone_number="2312311231",
                              external_user_id="123")

        mock_users.return_value = user_from_db
        patient = Patient(user_id=1)
        app = create_test_app()
        with app.app_context():
            with pytest.raises(InternalServerError) as e:
                self.patient_service.update_patient_data(user_from_req, "test@es.com", None, None, patient)

    @mock.patch.object(Users, "find_by_id")
    @mock.patch.object(UserRegister, "find_by_id", return_value=UserRegister(email="test1@es.com"))
    @mock.patch("services.patient_services.db.session")
    def test_update_patient_data_with_duplicate_email_error(self, mock_session, mock_register, mock_users):
        user_from_db = Users(first_name="Test",
                             last_name="Name",
                             phone_number="2312311231",
                             external_user_id="123")

        user_from_req = Users(first_name="Test_2",
                              last_name="Name_2",
                              phone_number="2312311231",
                              external_user_id="123")

        mock_users.return_value = user_from_db
        patient = Patient(user_id=1)
        app = create_test_app()
        with app.app_context():
            with pytest.raises(InternalServerError) as e:
                self.patient_service.update_patient_data(user_from_req, "test@es.com", None, None, patient)

    @mock.patch.object(Users, "find_by_id")
    @mock.patch.object(PatientsDevices, "find_record_by_patient_id",
                       return_value=PatientsDevices(patient_id=1, device_serial_number="1234567"))
    @mock.patch.object(UserRegister, "find_by_id", return_value=UserRegister(email="test@es.com"))
    @mock.patch.object(ProviderRoleTypes, "find_by_name")
    @mock.patch.object(PatientsProviders, "find_by_patient_and_role_id")
    @mock.patch.object(PatientsPatches, "find_by_patient_id")
    @mock.patch.object(PatientServices, "_PatientServices__check_patient_device_association")
    @mock.patch.object(PatientServices, "_PatientServices__update_patient_address")
    @mock.patch.object(PatientServices, "_PatientServices__update_patient_details")
    @mock.patch.object(PatientServices, "_PatientServices__update_patch_details")
    @mock.patch("services.patient_services.db.session")
    def test_update_patient_data_success(self, mock_session, mock_update_patch_details,
                                         mock_update_patient_details, mock_update_patient_address,
                                         mock_dev_association, mock_patients_patches,
                                         mock_pat_providers, mock_role_types, mock_find_by_id, mock_patient_device,
                                         mock_users):
        user_from_db = MagicMock(Users)

        user_from_req = Users(first_name="Test_2",
                              last_name="Name_2",
                              phone_number="2312311231",
                              external_user_id="123")

        patient_details = {
            "device": {
                "serial_number": "12345"
            },
            "facility": {"facility_id": 1},
            "providers": {
                "outpatient_provider_id": 5,
                "prescribing_provider_id": 3
            },
            "details": {
                "shoulder_strap_back": "1212121"
            },
            "patches": {
                "test": "1212121"
            }
        }

        mock_users.return_value = user_from_db
        patient = MagicMock(Patient)
        app = create_test_app()
        with app.app_context():
            self.patient_service.update_patient_data(user_from_req, "test@es.com", patient, patient_details, patient)


    @mock.patch("services.patient_services.db.session")
    def test_count_devices_assgined_returning_zero(self, mock_session):
        app = create_test_app()
        with app.app_context():
            count = self.patient_service.count_device_assigned(2)
            self.assertEqual(count, 0)

    # @mock.patch("services.patient_services.db.session")
    # def test_count_devices_assigned_returning_one(self, mock_session):
    #     mock_session.query.return_value.filter.return_value.all.return_value = ["123"]
    #
    #     app = create_test_app()
    #     with app.app_context():
    #         count = self.patient_service.count_device_assigned(1)
    #         self.assertEqual(count, 1)

    # @mock.patch("services.patient_services.db.session")
    # @mock.patch.object(DeviceManagerApi, "get_device_status", return_value="assigned")
    # def test_count_devices_assigned_returning_two(self, mock_deviceapi,  mock_session):
    #     mock_session.query.return_value.filter.return_value.all.return_value = ["123"]
    #
    #     app = create_test_app()
    #     with app.app_context():
    #         count = self.patient_service.count_device_assigned(1)
    #         self.assertEqual(count, 1)

    @mock.patch("services.patient_services.db.session")
    def test_patient_device_list_returning_empty(self, mock_session):
        mock_session.query.return_value.\
            join.return_value.\
            join.return_value. \
            join.return_value. \
            with_entities.return_value. \
            filter_by.return_value.\
            all.return_value = []

        app = create_test_app()
        with app.app_context():
            devices = self.patient_service.patient_device_list({"user_email": "abc.com"})
            self.assertEqual(len(devices), 0)

    @mock.patch("services.patient_services.db.session")
    @mock.patch.object(DeviceManagerApi, "get_device", return_value=PatientsDevices())
    def test_patient_device_list_returning_data(self, mock_deviceapi, mock_session):
        mock_session.query.return_value. \
            join.return_value. \
            join.return_value. \
            join.return_value. \
            with_entities.return_value. \
            filter_by.return_value. \
            all.return_value = ["1233", "21212"]

        app = create_test_app()
        with app.app_context():
            devices = self.patient_service.patient_device_list({"user_email": "abc.com"})
            self.assertEqual(len(devices), 2)

    @mock.patch("services.patient_services.db.session")
    def test_patient_device_association_check_same_serial_number(self, session):
        pd = PatientsDevices()
        pd.device_serial_number = 1234

        app = create_test_app()
        with app.app_context():
            devices = self.patient_service.\
                _PatientServices__check_patient_device_association(session, 1234, 1, pd)
            self.assertTrue(True)

    @mock.patch("services.patient_services.db.session")
    @mock.patch.object(PatientsDevices, "find_by_device_serial_number", return_value=True)
    def test_patient_device_association_check_device_in_use(self, session, mock_pat_dev):
        pd = PatientsDevices()
        pd.device_serial_number = 1235

        app = create_test_app()
        with app.app_context():
            with pytest.raises(Conflict) as e:
                devices = self.patient_service. \
                    _PatientServices__check_patient_device_association(session, 1234, 1, pd)


    @mock.patch("services.patient_services.db.session")
    @mock.patch("services.patient_services.PatientServices.count_device_assigned", return_value=1)
    @mock.patch.object(PatientsDevices, "find_by_device_serial_number", return_value=False)
    @mock.patch.object(DeviceManagerApi, "check_device_exists", return_value=True)
    @mock.patch.object(DeviceManagerApi, "update_device_status")
    def test_patient_device_association_check_device_count_less_than_2(self, session, dev_assigned,
                                                mock_pat_dev, mock_dev_api, mock_update_status):
        pd = PatientsDevices()
        pd.device_serial_number = 1235

        app = create_test_app()
        with app.app_context():
            session = self.patient_service. \
                _PatientServices__check_patient_device_association(session, 1234, 1, pd)

    @mock.patch("services.patient_services.db.session")
    @mock.patch.object(Address, "find_by_id")
    def test_update_patient_address(self, session, mock_address):
        pt_from_db = Patient()
        pt_from_db.permanent_address_id = 2
        pt_from_db.shipping_address_id = 1

        patient_in = MagicMock(Patient)

        app = create_test_app()
        with app.app_context():
            session = self.patient_service. \
                _PatientServices__update_patient_address(session, patient_in, pt_from_db)

    @mock.patch("services.patient_services.db.session")
    @mock.patch("services.patient_services.PatientServices.flush_db")
    @mock.patch("services.patient_services.PatientServices.commit_db")
    @mock.patch.object(Address, "find_by_id")
    def test_update_patient_address_no_address(self, session, flush, commit, mock_address):
        pt_from_db = Patient()
        patient_in = MagicMock()
        patient_in["permanent_address"].return_value = "1"

        app = create_test_app()
        with app.app_context():
            session = self.patient_service. \
                _PatientServices__update_patient_address(session, patient_in, pt_from_db)