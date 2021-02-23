import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from werkzeug.exceptions import InternalServerError


def send_otp(
        name: str, to_address: str,
        subject: str, otp: str):

    from_address = os.environ["SMTP_FROM"]
    print('address email', from_address)
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
            os.environ["SMTP_SERVER"],
            os.environ["SMTP_PORT"])
        server.starttls()
        server.login(os.environ["SMTP_USERNAME"], os.environ["SMTP_PASSWORD"])
        print('-------SMTP------------')
        print(os.environ["SMTP_USERNAME"], os.environ["SMTP_PASSWORD"])
        text = msg.as_string()
        server.sendmail(from_address, to_address, text)
        server.quit()
    except Exception as e:
        print("Something went wrong. {0}".format(e))
        raise InternalServerError("Something went wrong. {0}".format(e))
        return False
