import json
import io
import os
import logging
from sqlalchemy import cast, String
from collections import namedtuple
from datetime import datetime, timedelta

from db import db
from io import BytesIO
from docxtpl import DocxTemplate

from model.patient import Patient
from model.address import Address
from model.users import Users
from model.facilities import Facilities
from model.providers import Providers
from model.study_managers import StudyManagers
from model.patients_providers import PatientsProviders
from model.user_registration import UserRegister
from model.material_requests import MaterialRequests
from model.provider_role_types import ProviderRoleTypes
from model.providers_roles import ProviderRoles

from utils.common import format_phone_number
from utils.send_mail import send_product_request_email
from utils.constants import PDR_PROTOCOL_NUMBER, INITIAL_SHIPPING_DAYS, PRESCRIBING_PROVIDER, OUTPATIENT_PROVIDER
from utils.s3_api import S3Api

class MaterialRequestObj:
    def __init__(self):
        self.loggedin_user = ""
        self.today = datetime.now().strftime("%m/%d/%Y")
        self.date_requested = None
        self.needed_by_date = None
        self.sequence_number = ""
        self.recipient_name = ""
        self.site_name = ""
        self.address = ""
        self.city = ""
        self.state = ""
        self.zip = ""
        self.country = ""
        self.phone = ""
        self.email = ""
        self.patch_kit_qty = 0
        self.mdu_qty = 0
        self.starter_kit_qty = 0
        self.skin_prep_kit_qty = 0
        self.removal_kit_qty = 0
        self.placement_accessory_qty = 0
        self.ht_qty = 0
        self.ifu_qty = 0
        self.adhesive_laminate_qty = 0
        self.mdu_return_qty = 0
        self.patch_return_qty = 0
        self.placement_accessory_return_qty = 0
        self.return_label_qty = 0
        self.site_id = 0
        self.user_id = 0
        self.special_instructions = ""
        self.complaint_request = ""

    def count_items(self):
        count = self.patch_kit_qty + \
                self.mdu_qty + \
                self.starter_kit_qty + \
                self.skin_prep_kit_qty + \
                self.removal_kit_qty + \
                self.placement_accessory_qty + \
                self.ht_qty + \
                self.ifu_qty + \
                self.adhesive_laminate_qty + \
                self.patch_return_qty + \
                self.mdu_return_qty + \
                self.placement_accessory_return_qty + \
                self.return_label_qty
        return count

    def to_dict(self, data):
        for key in data:
            setattr(self, key, data[key])


class MaterialRequestService:
    def __init__(self):
        pass

    def send_initial_product_request(self, logged_in_user_email: str,
                                     patient: Patient,
                                     patient_email: str) -> bool:
        logging.info("Sending initial patient material request..")
        self.__send_patient_request(logged_in_user_email,
                                  patient, patient_email)

        logging.info("Sending study manager material request..")
        self.__send_csm_request(logged_in_user_email)

        logging.info("Sending site material request..")
        self.__send_site_request(logged_in_user_email, patient)

        return True

    def send_new_product_request(self, request_data: MaterialRequestObj,
                                 logged_in_user_email: str):
        # TODO Add additional logic here
        user = UserRegister.find_by_email(logged_in_user_email)

        material_requests_db = MaterialRequests()
        material_requests_db.num_items = request_data.count_items()
        material_requests_db.request_date = request_data.date_requested
        material_requests_db.requested_user_id = user.id
        material_requests_db.recipient = request_data.recipient_name

        if request_data.site_id > 0:
            material_requests_db.site_id = request_data.site_id

        if request_data.patient_id > 0:
            material_requests_db.patient_id = request_data.patient_id
        obj_from_db = material_requests_db.save_to_db()

        # Sequence number gets generated by the database
        request_data.sequence_number = obj_from_db.request_number

        self.__send_request(request_data.__dict__, logged_in_user_email)
        return True

    def get_filtered_material_list(self, page_number, record_per_page, request_number):
        """
            Return a list of all material requests
        """
        material_list = namedtuple(
            "MaterialsList",
            (
                "request_number",
                "request_id",
                "requestor",
                "date_requested",
                "recipient",
                "items_requested"
            ),
        )

        # Get all facilities and address
        requests_query = db.session.query(MaterialRequests)
        if request_number is not None and len(request_number) > 0:
            requests_query = requests_query.filter(cast(MaterialRequests.request_number, String).ilike(f'%{request_number}%'))

        data_count = requests_query.count()
        query_data = []
        lists = []
        try:
            query_data = (
                requests_query.order_by(MaterialRequests.request_number)
                    .paginate(page_number + 1, record_per_page).items
            )
        except Exception as e:
            logging.exception(e)

        for data in query_data:
            user = Users.find_by_id(data.requested_user_id)

            user_name = ""
            if user is not None:
                user_name = user.first_name + " " + user.last_name

            requests = material_list(
                request_number=data.request_number,
                request_id=data.id,
                requestor=user_name,
                date_requested=data.request_date,
                recipient=data.recipient,
                items_requested=data.num_items
            )

            lists.append(requests._asdict())

        return lists, data_count

    def __send_patient_request(self, logged_in_user_email, patient: Patient, patient_email):
        '''
            Two Patch Kits to be sent to patient's address upon patient registration
        '''
        req = MaterialRequestObj()

        try:
            user_obj = Users.find_by_email(logged_in_user_email)
            req.loggedin_user = user_obj.first_name + " " + user_obj.last_name

            material_requests_db = MaterialRequests()
            material_requests_db.num_items = 2
            material_requests_db.request_date = datetime.now()
            material_requests_db.requested_user_id = user_obj.id
            material_requests_db.recipient = patient.user.first_name + " " + patient.user.last_name
            material_requests_db.recipient_user_id = patient.user_id
            obj_from_db = material_requests_db.save_to_db()

            time = datetime.now() + timedelta(days=INITIAL_SHIPPING_DAYS)
            req.needed_by_date = time.strftime("%m/%d/%Y")

            # Sequence number gets generated by the database
            req.sequence_number = obj_from_db.request_number

            req.site_name = "N/A"
            # Find the patient name
            user = Users.find_by_id(patient.user_id)
            req.recipient_name = user.first_name + " " + user.last_name
            req.phone = format_phone_number(user.phone_number)
            req.email = patient_email

            # Since this is the first request, the product will be shipped to a patient.
            address = Address.find_by_id(patient.shipping_address_id)
            req.address = address.street_address_1
            req.city = address.city
            req.zip = address.postal_code
            req.country = address.country
            req.state = address.state

            req.patch_kit_qty = 2
            req.complaint_request = "No"
            req.special_instructions = "N/A"
            req_json = json.dumps(req.__dict__)
            logging.debug(req_json)

            self.__send_request(req.__dict__, logged_in_user_email)
        except Exception as e:
            logging.exception(e)
        return

    def __send_csm_request(self, logged_in_user_email):
        """
        Send one defib unit to the CSMs(the person who registers the patient) upon patient enrollment
        """
        req = MaterialRequestObj()

        try:
            user_obj = Users.find_by_email(logged_in_user_email)
            req.loggedin_user = user_obj.first_name + " " + user_obj.last_name

            material_requests_db = MaterialRequests()
            material_requests_db.num_items = 1
            material_requests_db.request_date = datetime.now()
            material_requests_db.requested_user_id = user_obj.id
            material_requests_db.recipient = user_obj.first_name + " " + user_obj.last_name
            material_requests_db.recipient_user_id = user_obj.id
            obj_from_db = material_requests_db.save_to_db()

            time = datetime.now() + timedelta(days=INITIAL_SHIPPING_DAYS)
            req.needed_by_date = time.strftime("%m/%d/%Y")

            # Sequence number gets generated by the database
            req.sequence_number = obj_from_db.request_number

            req.site_name = "N/A"
            # Logged in user is the CSM
            req.recipient_name = user_obj.first_name + " " + user_obj.last_name
            req.phone = format_phone_number(user_obj.phone_number)
            req.email = logged_in_user_email

            # Since this is the site manager, get the address
            sm = StudyManagers.find_by_user_id(_user_id=user_obj.id)
            address = None
            if sm is not None:
                address = Address.find_by_id(sm.address_id)

            if address is not None:
                req.address = address.street_address_1
                req.city = address.city
                req.zip = address.postal_code
                req.country = address.country
                req.state = address.state
                req.special_instructions = "N/A"
            else:
                req.special_instructions = "Could not find the address for the study manager"

            req.mdu_qty = 1
            req.complaint_request = "No"
            req_json = json.dumps(req.__dict__)
            logging.debug(req_json)

            self.__send_request(req.__dict__, logged_in_user_email)
        except Exception as e:
            logging.exception(e)
        return

    def __send_site_request(self, logged_in_user_email, patient: Patient):
        """
            One Starter Kit and two Patch Kits to be sent to the site where the patient was enrolled
        """
        req = MaterialRequestObj()

        try:
            user_obj = Users.find_by_email(logged_in_user_email)
            req.loggedin_user = user_obj.first_name + " " + user_obj.last_name

            # Get the site information for the patient
            provider_facility = db.session.query(Facilities, Providers, PatientsProviders, Patient) \
                .join(PatientsProviders, PatientsProviders.patient_id == Patient.id) \
                .join(Providers, PatientsProviders.provider_id == Providers.id) \
                .join(Facilities, Providers.facility_id == Facilities.id) \
                .filter(Patient.id == patient.id).all()

            primary_provider = None
            facility = None
            if provider_facility is None:
                logging.error("Could not find the facility information.")
            else:
                facility = provider_facility[0][0]

                providers = Providers.find_by_facility_id(facility.id)

                # Find the primary study coordinator
                for provider in providers:
                    if provider.is_primary:
                        primary_provider = provider

            material_requests_db = MaterialRequests()
            material_requests_db.num_items = 3
            material_requests_db.request_date = datetime.now()
            material_requests_db.requested_user_id = user_obj.id

            if facility is not None:
                material_requests_db.recipient = facility.name
                material_requests_db.site_id = facility.id

            obj_from_db = material_requests_db.save_to_db()

            time = datetime.now() + timedelta(days=INITIAL_SHIPPING_DAYS)
            req.needed_by_date = time.strftime("%m/%d/%Y")

            # Sequence number gets generated by the database
            req.sequence_number = obj_from_db.request_number

            # This request is going to the site. Use the outpatient provider name
            if primary_provider is not None:
                req.recipient_name = primary_provider.user.first_name + " " \
                                     + primary_provider.user.last_name
            else:
                req.recipient_name = user_obj.first_name + " " + user_obj.last_name
            req.phone = format_phone_number(primary_provider.user.phone_number)
            req.email = primary_provider.user.registration.email

            if facility is not None:
                req.site_name = facility.name

                # Since this is the site, get the facility address
                address = Address.find_by_id(facility.address_id)
                req.address = address.street_address_1
                req.city = address.city
                req.zip = address.postal_code
                req.country = address.country
                req.state = address.state

            req.starter_kit_qty = 1
            req.patch_kit_qty = 2
            req.complaint_request = "No"
            req.special_instructions = "N/A"
            req_json = json.dumps(req.__dict__)
            logging.debug(req_json)

            self.__send_request(req.__dict__, logged_in_user_email)
        except Exception as e:
            logging.exception(e)
        return

    def __send_request(self, request_data, logged_in_user_email):
        template_file = os.path.join(os.getcwd(), "templates", "PRD_template.docx")
        logging.info(f"template file: {str(template_file)}")
        content = self.__doc_from_template(template_file, request_data)
        csv_file = self.__generate_excel(request_data)
        send_product_request_email(request_data["sequence_number"],
                                   content.read(), csv_file.read(), logged_in_user_email)

        content.seek(0)
        csv_file.seek(0)
        csv_file_buff = io.BytesIO(csv_file.getvalue().encode())
        s3api = S3Api()
        s3api.upload_material_request_form(request_data["sequence_number"],
                                           content, csv_file_buff)

    def __doc_from_template(self, template_file, data):
        template = DocxTemplate(template_file)
        template.render(data)

        docx_stream = BytesIO()
        template.save(docx_stream)
        docx_stream.seek(0)

        return docx_stream

    def __generate_excel(self, data_dict):
        import csv
        from io import StringIO
        header = ["Transaction #", "Requested By", "Date Requested", "Date Needed",
                  "Protocol #", "Recipient Shipping Information", "Recipient Phone #",
                  "Recipient Email Address", "Patch Kit", "ES-2 Defibrillator Unit MDU",
                  "ES-2 Starter Kit", "Skin Prep Kit", "Removal Kit", "Placement Accessory",
                  "Hair Trimmer", "Jewel Patient Guide, ES-2 Device", "Adhesive Laminate",
                  "MDU return material", "Patch-Kit return materia",
                  "Placement Accessory return material", "Return Labels (x6)"]

        data = MaterialRequestObj()
        data.to_dict(data_dict)
        address = data.address + ", " + data.city + ", " + data.state + ", " + data.zip + ", " + data.country
        csv_data = [data.sequence_number, data.loggedin_user, data.today, data.needed_by_date,
                    PDR_PROTOCOL_NUMBER, address, format_phone_number(data.phone), data.email, data.patch_kit_qty,
                    data.mdu_qty, data.starter_kit_qty, data.skin_prep_kit_qty, data.removal_kit_qty,
                    data.placement_accessory_qty, data.ht_qty, data.ifu_qty, data.adhesive_laminate_qty,
                    data.mdu_return_qty, data.patch_return_qty, data.placement_accessory_return_qty,
                    data.return_label_qty]
        # TODO: Update this once the protocol template is finalized
        f = StringIO()
        csv.writer(f).writerow(header)
        csv.writer(f).writerow(csv_data)
        f.seek(0)
        return f
