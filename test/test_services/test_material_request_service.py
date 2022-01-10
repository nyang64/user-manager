from test.flask_app1 import create_test_app
from unittest import TestCase, mock
from unittest.mock import MagicMock

from services.material_request_services import MaterialRequestService, MaterialRequestObj
from model.address import Address
from model.material_requests import MaterialRequests
from model.patient import Patient
from model.study_managers import StudyManagers
from model.user_registration import UserRegister
from model.users import Users

from db import db


class TestMaterialRequestServices(TestCase):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.service = MaterialRequestService()

    def setUp(self):
        app = create_test_app()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        app = create_test_app()
        with app.app_context():
            db.session.remove()
            db.drop_all()

    @mock.patch.object(MaterialRequestService, "_MaterialRequestService__send_patient_request")
    @mock.patch.object(MaterialRequestService, "_MaterialRequestService__send_csm_request")
    @mock.patch.object(MaterialRequestService, "_MaterialRequestService__send_site_request")
    def test_send_initial_product_request(self, mock_site, mock_csm, mock_pt):
        self.service.send_initial_product_request("test@", MagicMock(), "test@")
        self.assertTrue(True)

    @mock.patch.object(UserRegister, "find_by_email", return_value=UserRegister())
    @mock.patch.object(MaterialRequests, "save_to_db")
    @mock.patch.object(MaterialRequestService, "_MaterialRequestService__send_request")
    def test_send_new_product_request(self, mock_reg, mock_req, mock_req_svc):
        data = MaterialRequestObj()
        data.patient_id = 1

        app = create_test_app()
        with app.app_context():
            self.service.send_new_product_request(data, "test@")
            self.assertTrue(True)

    @mock.patch("services.patient_services.db.session")
    @mock.patch.object(Users, "find_by_id")
    def test_filtered_list(self, mock_user, mock_ses):
        item = MaterialRequests()
        item.requested_user_id = 1
        item.request_number = 12345
        item.id = 1
        item.request_date = "12-12-2021"
        item.recipient = "Joe"
        item.num_items = 2

        user = Users()
        user.first_name = "test"
        user.last_name = "user"

        mock_ses.query.return_value.order_by.return_value.paginate.return_value.\
            items = [item]
        mock_ses.query.return_value.count.return_value = 1
        mock_user.return_value = user

        app = create_test_app()
        with app.app_context():
            data_list, count = self.service.get_filtered_material_list(page_number=1, record_per_page=5, request_number=None)
            self.assertTrue(True)
            self.assertEqual(count, 1)
            self.assertEqual(len(data_list), 1)

    @mock.patch.object(MaterialRequestService, "_MaterialRequestService__send_request")
    @mock.patch.object(Address, "find_by_id")
    @mock.patch.object(MaterialRequests, "save_to_db")
    @mock.patch.object(Users, "find_by_id")
    @mock.patch.object(Users, "find_by_email")
    def test_send_patient_request(self, usr_email, usr_id, mock_req, mock_addr, mock_srvc):
        user = Users()
        user.id = 1
        user.first_name = "test"
        user.last_name = "user"

        pt = Patient()
        pt.user = user
        pt.user_id = 1

        req = MaterialRequests()
        req.request_number = 12345

        usr_email.return_value = user
        usr_id.return_value = user
        mock_req.return_value = req

        addr = Address()
        addr.city = "test"
        addr.street_address_1 = "12333"
        addr.postal_code = "12345"
        addr.country = "US"
        addr.state = "CA"
        mock_addr.return_value = addr

        app = create_test_app()
        with app.app_context():
            self.service.\
                _MaterialRequestService__send_patient_request("j@e.com", pt, "test.t.com")
            self.assertTrue(True)
            mock_srvc.assert_called()

    @mock.patch.object(MaterialRequestService, "_MaterialRequestService__send_request")
    @mock.patch.object(Address, "find_by_id")
    @mock.patch.object(MaterialRequests, "save_to_db")
    @mock.patch.object(StudyManagers, "find_by_user_id")
    @mock.patch.object(Users, "find_by_email")
    def test_send_csm_request(self, usr_email, mock_sm, mock_req, mock_addr, mock_srvc):
        user = Users()
        user.id = 1
        user.first_name = "test"
        user.last_name = "user"

        pt = Patient()
        pt.user = user
        pt.user_id = 1

        req = MaterialRequests()
        req.request_number = 12345

        addr = Address()
        addr.city = "test"
        addr.street_address_1 = "12333"
        addr.postal_code = "12345"
        addr.country = "US"
        addr.state = "CA"

        sm = StudyManagers()
        sm.address_id = 1

        usr_email.return_value = user
        mock_sm.return_value = sm
        mock_req.return_value = req
        mock_addr.return_value = addr

        app = create_test_app()
        with app.app_context():
            self.service. \
                _MaterialRequestService__send_csm_request("j@e.com")
            self.assertTrue(True)
            mock_srvc.assert_called()
