from utils.send_mail import send_otp, send_registration_email
import pytest


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
    yield name, to_address, subject, username, password


class TestSendEmail:
    # Test Cases For Send OTP
    # def test_send_otp_with_parameter(self, email_var_otp):
    #     assert send_otp(
    #         email_var_otp[0],
    #         email_var_otp[1],
    #         email_var_otp[2],
    #         email_var_otp[3]) is True

    def test_send_otp_with_invalid_parameter(self, email_var_otp):
        with pytest.raises(Exception) as e:
            assert send_otp(
                email_var_otp[0],
                None,
                email_var_otp[2],
                email_var_otp[3])
        assert "500 Internal Server Error" in str(e.value)

    # def test_send_registration_with_parameter(self, email_var):
    #     assert send_registration_email(
    #         email_var[0],
    #         email_var[1],
    #         email_var[2],
    #         email_var[3],
    #         email_var[4]) is True

    def test_send_registration_with_invalid_parameter(self, email_var):
        with pytest.raises(Exception) as e:
            assert send_registration_email(
                email_var[0],
                None,
                email_var[2],
                email_var[3],
                email_var[4])
        assert "500 Internal Server Error" in str(e.value)
