from test.flask_app1 import create_test_app
from unittest import TestCase, mock

import json

from resources.device_manager import DeviceManager
from schema.device_ui_status_schema import DeviceUiStatusSchema
from model.device_ui_status_type import DeviceUiStatusType
from services.device_manager_api import DeviceManagerApi

create_status_string = """
{
    "device_serial_number": "12111211",
    "received_at": "2021-04-12T22:45:53Z",
    "statuses": [
        {
            "recorded_at": "2021-04-12T22:44:57.837Z",
             "ui_id": "S033"
        },
        {
            "ui_id": "S012",
            "recorded_at": "2021-04-12T22:45:47.204Z"
        }
    ],
    "receiver_id": "38c42174cf9b4c7db218d7740e929e0e"
}
"""

class TestDeviceManager(TestCase):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.device_mgr = DeviceManager()
        self.create_status_message_body = json.loads(create_status_string)

    @mock.patch("resources.device_manager.request", spec={})
    @mock.patch.object(DeviceUiStatusSchema, "load")
    def test_create_status_with_no_input(self, mock_status, mock_req):
        app = create_test_app()
        mock_req.json = {"newpassword": "asd"}
        with app.test_request_context():
            resp = self.device_mgr.create_status.__wrapped__(self.device_mgr, "")
            self.assertTrue(resp[1], 201)

    @mock.patch("resources.device_manager.request", spec={})
    @mock.patch.object(DeviceUiStatusSchema, "load")
    @mock.patch.object(DeviceUiStatusType, "find_by_ui_id")
    def test_create_status_with_status_input(self, mock_status, mock_status_schema, mock_req):
        app = create_test_app()
        mock_req.json = self.create_status_message_body
        with app.test_request_context():
            resp = self.device_mgr.create_status.__wrapped__(self.device_mgr, "")
            self.assertTrue(resp[1], 201)

    @mock.patch("utils.validation.request", spec={})
    def test_create_metric_with_no_device_serial_number(self, mock_req):
        app = create_test_app()
        mock_req.is_json = True
        mock_req.json = {"newpassword": "asd"}
        with app.test_request_context():
            resp = self.device_mgr.create_metric.__wrapped__(self.device_mgr, "")
            self.assertTrue(resp[1], 400)

    @mock.patch("utils.validation.request", spec={})
    @mock.patch("resources.device_manager.DeviceManagerApi.get_device", return_value={"key": None})
    def test_create_metric_with_no_encryption_key(self, mock_device_mgr, mock_req):
        app = create_test_app()
        mock_req.is_json = True
        mock_req.json = {"device_serial_number": "12345"}
        with app.test_request_context():
            resp = self.device_mgr.create_metric.__wrapped__(self.device_mgr, "")
            self.assertTrue(resp[1], 400)

    @mock.patch("utils.validation.request", spec={})
    @mock.patch("resources.device_manager.DeviceManagerApi.get_device", return_value={"key": "12344444"})
    @mock.patch("resources.device_manager.get_metrics_data")
    @mock.patch("resources.device_manager.parse_metrics")
    def test_create_metric_success_with_no_metrics_data(self, mock_parse, mock_metrics, mock_device_mgr, mock_req):
        app = create_test_app()
        mock_req.is_json = True
        mock_req.json = {"device_serial_number": "12345"}
        with app.test_request_context():
            resp = self.device_mgr.create_metric.__wrapped__(self.device_mgr, "")
            self.assertTrue(resp[1], 201)

    @mock.patch("utils.validation.request", spec={})
    @mock.patch("resources.device_manager.DeviceManagerApi.get_device", return_value={"key": "12344444"})
    @mock.patch("resources.device_manager.get_metrics_data")
    @mock.patch("resources.device_manager.parse_metrics")
    def test_create_metric_success_with_metrics_data(self, mock_parse, mock_metrics, mock_device_mgr, mock_req):
        app = create_test_app()
        mock_req.is_json = True
        mock_req.json = {"device_serial_number": "12345"}
        with app.test_request_context():
            resp = self.device_mgr.create_metric.__wrapped__(self.device_mgr, "")
            self.assertTrue(resp[1], 201)