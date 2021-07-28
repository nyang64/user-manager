from datetime import datetime, timezone, timedelta
import os
from flask import render_template
from shutil import rmtree

from model.user_registration import UserRegister
from model.newsletters import Newsletters
from services.repository.db_repositories import DbRepository
from services.user_services import UserServices
from utils import send_mail
from utils.s3_api import S3Api


class NewsletterServices(DbRepository):

    def __init__(self, _db, _app):
        self.db = _db
        self.app = _app
        self.valid_days = []
        self.valid_days = {}

    def deliver_newsletters(self):
        enrolled_users = self.find_enrolled_users()

        # Create a temporary folder for HTML test_templates to be rendered in
        local_location = os.getcwd() + "/templates/"
        self._create_local_directory_for_files(local_location=local_location)
        print(f"Download HTML files from S3")
        # Call S3Api and construct the html body
        S3Api.download_html_template(local_location)
        print(f"Done downloading HTML files from S3")

        # Retrieve all valid days
        for html_file in os.listdir(local_location):
            if html_file.startswith("day"):
                valid_html_file = html_file
                valid_day = valid_html_file.split("-")[1]
                self.valid_days[valid_day] = {}
                self.valid_days[valid_day]["HTML_FILE"] = valid_html_file
                self.valid_days[valid_day]["SUBJECT_LINE"] = \
                    valid_html_file.split(".")[0].replace("-", " ").capitalize()

        # Iterate through newsletters records to check if users need emails
        # user_id = user_id column in newsletters table -> should also be general user_id
        for user_id in enrolled_users:
            user_obj = UserServices.get_user_by_user_id(user_id=user_id)
            user_reg_obj = UserRegister.find_by_id(reg_id=user_obj.registration_id)
            print(f"Check enrolled user: {user_id}")

            # Calculate and check whether to deliver email to current user
            newsletter_user = Newsletters.find_by_user_id(_user_id=user_obj.id)
            newsletter_check, newsletter_day = self.can_send_newsletter(newsletter_obj=newsletter_user)

            if newsletter_check:
                # Construct the dynamic html page for email body
                html_file_body = self.construct_html_body(file_day=newsletter_day, user=user_obj)
                subject_line = self.valid_days[str(newsletter_day)]["SUBJECT_LINE"]

                # Send newsletter email to recipient
                send_mail.send_newsletter_email(html_body=html_file_body,
                                                subject_line=subject_line,
                                                user_reg_obj=user_reg_obj)
                # Update newsletter record in db
                self.update_newsletter_day_at(newsletter_obj=newsletter_user, new_day=newsletter_day)

        # Destroy temporary local_location
        self._destroy_local_location(local_location)

    def find_enrolled_users(self):
        with self.db.app.app_context():
            user_ids = []
            newsletters = Newsletters.all_records()
            for newsletter in newsletters:
                user_ids.append(newsletter.user_id)

            return user_ids

    def _create_local_directory_for_files(self, local_location):
        if not os.path.exists(local_location):
            os.makedirs(local_location)

    def _destroy_local_location(self, local_location):
        try:
            rmtree(local_location, ignore_errors=True)
        except Exception as e:
            print("Unable to remove temporary_images folder")
            raise e

    def can_send_newsletter(self, newsletter_obj) -> (bool, int):
        newsletter_day_at = newsletter_obj.day_at
        created_time = newsletter_obj.created_at

        # load current time with timezone
        current_time = datetime.now(tz=timezone.utc)

        # get time difference from when created
        time_delta = current_time - created_time
        day = time_delta.days
        print(f"current_day_at: {newsletter_day_at}")
        print(f"time_delta: {time_delta.days}")

        # Newsletters not send daily, check if day_at differs and if day_at is valid
        if day is not newsletter_day_at and str(day) in self.valid_days:
            return True, day
        elif day == "done":
            return True, "done"

        return False, day

    def update_newsletter_day_at(self, newsletter_obj, new_day):
        with self.db.app.app_context():
            newsletter_obj.day_at = new_day
            self.flush_db(newsletter_obj)
            self.commit_db()

    def construct_html_body(self, file_day, user):
        template_path = self.valid_days[str(file_day)]["HTML_FILE"]
        print(f"template path: {template_path}")

        # Other render variables
        survey_link = os.environ.get("SURVEY_LINK")

        # Using Flask app context, render day html template
        with self.app.app_context():
            rendered_html_body = render_template(
                template_path, user=user, survey_link=survey_link
            )

        return rendered_html_body
