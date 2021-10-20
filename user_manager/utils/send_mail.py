import os
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import render_template
from werkzeug.exceptions import InternalServerError
from shutil import rmtree

from config import read_environ_value
from utils.s3_api import S3Api
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

    # Fetch app instructions html from S3 bucket
    print(f"Download app instructions from S3 bucket")
    local_location = os.getcwd() + "/templates/"
    if not os.path.exists(local_location):
        os.makedirs(local_location)

    # Call S3Api and construct the html body
    S3Api.download_app_instructions(local_location)
    print(f"Done downloading HTML files from S3")
    template_path = "app-instructions.html"

    # Construct html template body
    testflight_link = read_environ_value(value, "TESTFLIGHT_LINK")
    link = read_environ_value(value, 'APP_LINK')

    rendered_html_body = render_template(
        template_path, app_link=link, testflight=testflight_link, username=username, password=password
    )

    msg.attach(MIMEText(rendered_html_body, 'html'))
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
        rmtree(local_location, ignore_errors=True)
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

    body = MIMEText(html_body, "html")
    msg.attach(body)

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


def send_user_registration_email(first_name, last_name, to_address,
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
              You have been assigned as a user in Element Science Patient Management System.
            </p>
            <p>URL for the portal is: {}</p>
            <p>
              Login with the credentials:<br/>
                        username: {}
                        password: {}
            </p>
          </body>
        </html>
        """.format(first_name, last_name, read_environ_value(value, 'MANAGEMENT_PORTAL_URL'),
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