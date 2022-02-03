import pytest
import os
from utils.send_mail import send_otp, \
    send_patient_registration_email, \
    send_newsletter_email, \
    send_user_registration_email, \
    send_product_request_email
from unittest import mock
from model.user_registration import UserRegister

from utils.s3_api import S3Api

@pytest.fixture
def email_var_otp():
    name = "Yogendra"
    to_address = "yogendra.rai@infostretch.com"
    subject = "test subject"
    otp = "111111"
    yield name, to_address, subject, otp


@pytest.fixture
def email_var():
    name = "Yogendra"
    to_address = "yogendra.rai@infostretch.com"
    subject = "test subject"
    username = "yogendra.rai"
    password = "12345678"
    body = "Test body"
    yield name, to_address, subject, username, password, body


class TestSendEmail:

    def test_send_otp_with_invalid_parameter(self, email_var_otp):
        with pytest.raises(Exception) as e:
            assert send_otp(email_var_otp[0], None, email_var_otp[2], email_var_otp[3])
        assert "500 Internal Server Error" in str(e.value)

    @mock.patch.object(S3Api, "download_app_instructions")
    @mock.patch("utils.send_mail.render_template")
    def test_send_registration_with_invalid_parameter(self, mock_s3_api, mock_template, email_var):
        with pytest.raises(Exception) as e:
            assert send_patient_registration_email(
                email_var[0], None, email_var[2], email_var[3], email_var[4]
            )
        assert "500 Internal Server Error" in str(e.value)

    @mock.patch("utils.send_mail.smtplib")
    def test_send_newsletter_email(self, mock_smtp, email_var):
        ur = UserRegister()
        ur.email = email_var[1]
        sent = send_newsletter_email(email_var[5], email_var[2], ur)
        assert sent is True
        assert mock_smtp.sendmail.called_once()

    @mock.patch("utils.send_mail.smtplib")
    def test_send_user_registration_email(self, mock_smtp, email_var):
        ur = UserRegister()
        ur.email = email_var[1]
        sent = send_user_registration_email("Test", "patient", email_var[0],
                                            email_var[3], email_var[4])
        assert sent is True
        assert mock_smtp.sendmail.called_once()

    @mock.patch("utils.send_mail.smtplib")
    @mock.patch("utils.send_mail.CUSTOMER_SERVICE_EMAIL", "tes123t@")
    def test_send_product_request_email(self, mock_email, email_var):
        sent = send_product_request_email(1, "", "", "test@")
        assert sent is True
