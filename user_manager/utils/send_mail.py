import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from werkzeug.exceptions import InternalServerError
from config import read_environ_value
import os
import logging
value = os.environ.get('SECRET_MANAGER_ARN')




def send_otp(
        name: str, to_address: str,
        subject: str, otp: str):

    from_address = read_environ_value(value, "SMTP_FROM")
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = "Notification: {}".format(subject)
    body = """



    Hello {0},



    {1} is Your ES-Cloud OTP. OTP is confidential.
    For Security Reasons, DO NOT share this OTP with anyone.



    Thanks & Regards,

    Me



    """.format(name, otp)
    msg.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP(
            read_environ_value(value, "SMTP_SERVER"),
            read_environ_value(value, "SMTP_PORT"))
        server.starttls()
        server.login(read_environ_value(value, "SMTP_USERNAME"),
                     read_environ_value(value, "SMTP_PASSWORD"))
        text = msg.as_string()
        server.sendmail(from_address, to_address, text)
        server.quit()
        return True
    except Exception as e:
        logging.error(e)
        raise InternalServerError("Something went wrong. {0}".format(e))
        return False


def send_registration_email(
        first_name: str, to_address: str,
        subject: str, username: str, password: str):

    from_address = read_environ_value(value, "SMTP_FROM")
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = "{}".format(subject)
    body = """
    Hello {},


     <h1>Welcome to Element Science</h1>
        <p>The ES-2 Jewel app is a mobile app accessory to the Jewel device.
        This version of the mobile app will display current Jewel
        device status.</p>


    <h1>App download instructions</h1>
    <p>
    <ul>
        <li>Download and install the app using the link {}
        <li>Install the app
        <li>Login with the credentials:<br/>
                username: {}
                password: {}
    </ul></p>
    """.format(first_name, read_environ_value(value, 'APP_LINK'),
               username, password)
    msg.attach(MIMEText(body, 'html'))
    try:
        server = smtplib.SMTP(
            read_environ_value(value, "SMTP_SERVER"),
            read_environ_value(value, "SMTP_PORT"))
        server.starttls()
        server.login(read_environ_value(value, "SMTP_USERNAME"),
                     read_environ_value(value, "SMTP_PASSWORD"))
        text = msg.as_string()
        server.sendmail(from_address, to_address, text)
        server.quit()
        return True
    except Exception as e:
        logging.error(e)
        raise InternalServerError("Something went wrong. {0}".format(e))
