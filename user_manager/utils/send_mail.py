import os
import logging
import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from flask import render_template
from werkzeug.exceptions import InternalServerError

from config import read_environ_value
from utils.s3_api import S3Api
from utils.constants import CUSTOMER_SERVICE_EMAIL, PATIENT, PROVIDER

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
    <html>
          <head>
          Element Science
          </head>
          <body>
            Hello {0},
        
            <p>{1} is Your ES-Cloud OTP. OTP is confidential. </p>
            <p>For Security Reasons, DO NOT share this OTP with anyone.</p>
        </body>
    </html>
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
            <p>Login with the credentials:
            <br>username: {} </br>
            <br>password: {} </br>
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


def send_product_request_email(seq_number, docx_content, csv_content, sender):
    logging.info("Sending email.")
    from_address = read_environ_value(value, "SMTP_FROM")
    receivers_mail = [CUSTOMER_SERVICE_EMAIL, sender]
    to_address = ", ".join(receivers_mail)
    msg = MIMEMultipart()

    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = f"Product Request Form - R{seq_number}"
    body = MIMEText(f"Product Request Form", "html")
    msg.attach(body)

    part = MIMEBase("application", "octate-stream")
    part.set_payload(docx_content)
    encoders.encode_base64(part)
    part.add_header("Content-Disposition",
                    f"attachment; filename=ProductRequestForm-{seq_number}.docx")
    msg.attach(part)

    part1 = MIMEBase("application", "octate-stream")
    part1.set_payload(csv_content)
    encoders.encode_base64(part1)
    part1.add_header("Content-Disposition", f"attachment; filename=ProductRequestForm-{seq_number}.csv")
    msg.attach(part1)

    try:
        server = smtplib.SMTP(
            read_environ_value(value, "SMTP_SERVER"),
            read_environ_value(value, "SMTP_PORT"))
        server.starttls()
        server.login(read_environ_value(value, "SMTP_USERNAME"),
                     read_environ_value(value, "SMTP_PASSWORD"))
        print(f"sending email to: {to_address}")
        server.sendmail(from_address, to_address, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        logging.error(e)
        raise InternalServerError("Something went wrong. {0}".format(e))


def send_password_reset_email(first_name, last_name, to_address, username, password,
                              send_to_cs, role):
    from_address = read_environ_value(value, "SMTP_FROM")
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = "Password reset"
    if send_to_cs is True:
        msg['Cc'] = CUSTOMER_SERVICE_EMAIL

    app_url = None
    testflight_url = None

    if role == PATIENT:
        testflight_url = read_environ_value(value, "TESTFLIGHT_LINK")
        app_url = read_environ_value(value, "APP_LINK")
    elif role == PROVIDER:
        app_url = read_environ_value(value, "CLINICAL_PORTAL_URL")

    body = """
        <html>
          <body>
              Hello {} {},
              <p>
                  Please use the below credentials for login. If you did not initiate the request for password, please 
                  call 1-800-985-5702 to report the incident. 
             </p>
            <br>Username: {} </br>
            <br>Password: {} </br>
            """
    if testflight_url is not None:
        body += """
                <br>Test Flight Link: {} </br>
               """
    if app_url is not None:
        body += """
            <br>Application Link: {} </br>
            <br>
            """
    body += """
            </p>
          </body>
        </html>
        """

    if testflight_url is not None:
        body = body.format(first_name, last_name, username, password, testflight_url, app_url)
    elif app_url is not None:
        body = body.format(first_name, last_name, username, password, app_url)
    else:
        body = body.format(first_name, last_name, username, password)

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
