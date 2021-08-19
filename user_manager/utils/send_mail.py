import os
import logging
import boto3
import smtplib
from html2image import Html2Image
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from werkzeug.exceptions import InternalServerError

from config import read_environ_value
from utils.constants import PATIENT, PROVIDER

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


def send_patient_registration_email(
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


def send_newsletter_email(html_body, subject_line, user_reg_obj):
    from_address = read_environ_value(value, "SMTP_FROM")
    to_address = user_reg_obj.email
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject_line

    # Convert HTML string to PNG image and attach to email body
    hti = Html2Image(
        custom_flags=['--no-sandbox']
    )
    hti.screenshot(html_body, save_as="day.png", size=(600, 1892))

    # Attach image to text for email body
    text = MIMEText('<img src="cid:image1" class="center">', 'html')
    msg.attach(text)
    image = MIMEImage(open('day.png', 'rb').read())

    # Define the image's ID as referenced in the HTML body above
    image.add_header('Content-ID', '<image1>')
    msg.attach(image)

    #TESTING
    # body = MIMEText(html_body, "html")
    # msg.attach(body)

    try:
        server = smtplib.SMTP(
            read_environ_value(value, "SMTP_SERVER"),
            read_environ_value(value, "SMTP_PORT"))
        server.starttls()
        server.login(read_environ_value(value, "SMTP_USERNAME"),
                     read_environ_value(value, "SMTP_PASSWORD"))
        text = msg.as_string()
        print(f"sending email to: {to_address}")
        server.sendmail(from_address, to_address, text)
        server.quit()
        return True
    except Exception as e:
        logging.error(e)
        raise InternalServerError("Something went wrong. {0}".format(e))


def send_provider_registration_email(first_name, last_name, to_address,
                                        username, password):
    from_address = read_environ_value(value, "SMTP_FROM")
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = "Welcome to Element Science"
    body = """
        <html>
          <head>
          Element Science
          </head>
          <body>
            <h1>Welcome to Element Science</h1>
            <p>Dear {} {},</p>
            <p></p>
            <p>
              You have been assigned as a user in Element Science clinical portal.
            </p>
            <p>URL for the portal is: {}</p>
            <p>
              Login with the credentials:<br/>
                        username: {}
                        password: {}
            </p>
          </body>
        </html>
        """.format(first_name, last_name, read_environ_value(value, 'CLINICAL_PORTAL_URL'),
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
        print(f"sending email to: {to_address}")
        server.sendmail(from_address, to_address, text)
        server.quit()
        return True
    except Exception as e:
        logging.error(e)
        raise InternalServerError("Something went wrong. {0}".format(e))