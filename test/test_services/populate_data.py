import uuid

from db import db
from model.address import Address
from model.facilities import Facilities
from model.patient import Patient
from model.patients_devices import PatientsDevices
from model.provider_role_types import ProviderRoleTypes
from model.providers import Providers
from model.roles import Roles
from model.salvos import Salvos
from model.therapy_reports import TherapyReport
from model.user_registration import UserRegister
from model.user_status_type import UserStatusType
from model.users import Users


class PopulateData:
    def __init__(self):
        pass

    def register_user(self, email):
        reg_data = UserRegister(email=email, password="password")
        db.session.add(reg_data)
        db.session.commit()
        return reg_data

    def create_user(self, email):
        reg = self.register_user(email)
        user_data = Users(
            first_name="first_name",
            last_name="last_name",
            phone_number="phone_number",
            registration_id=reg.id,
            uuid=uuid.uuid4(),
        )
        db.session.add(user_data)
        db.session.commit()
        return user_data

    def create_patient(self, email):
        self.register_user(email)
        user = self.create_user("user@gmail.com")
        patient_data = Patient(
            user_id=user.id,
            emergency_contact_name="emer",
            emergency_contact_number="emer_cnt",
            date_of_birth="29/12.1997",
            gender="male",
            indication="In",
        )
        db.session.add(patient_data)
        db.session.commit()
        return patient_data

    def create_provider(self, email):
        user = self.create_user(email)
        facility = self.create_facility()
        provider_data = Providers(user_id=user.id, facility_id=facility.id)
        db.session.add(provider_data)
        db.session.commit()
        return provider_data

    def create_therapy_report(self):
        patient = self.create_patient("patient@gmail.com")
        therapy = TherapyReport(patient_id=patient.id, device_serial_number="12")
        db.session.add(therapy)
        db.session.commit()
        return therapy

    def create_salvos_report(self):
        therapy = self.create_therapy_report()
        salvos = Salvos(therapy_report_id=therapy.id, pdf_location="/KEY")
        db.session.add(salvos)
        db.session.commit()
        return salvos

    def add_patient_device(self, number):
        patient = self.create_patient("patient_device@gmail.com")
        devices = PatientsDevices(patient_id=patient.id, device_serial_number=number)
        db.session.add(devices)
        db.session.commit()
        return devices

    def create_address(self):
        address = Address(
            street_address_1="Ad",
            street_address_2="Ae",
            city="Kl",
            state="MH",
            country="IN",
            postal_code="421306",
        )
        db.session.add(address)
        db.session.commit()
        return address

    def create_facility(self):
        address = self.create_address()
        facility = Facilities(
            address_id=address.id, on_call_phone="9090909090", name="faci"
        )
        db.session.add(facility)
        db.session.commit()
        return facility

    def add_roles(self):
        from utils.constants import ADMIN, PROVIDER, ESUSER, PATIENT

        roles = [
            Roles(role_name=ADMIN),
            Roles(role_name=PROVIDER),
            Roles(role_name=ESUSER),
            Roles(role_name=PATIENT),
        ]
        db.session.add_all(roles)
        db.session.commit()

    def add_user_status_types(self):
        from utils.constants import DISABLED, ACTIVE, SUSPENDED, ENROLLED, DISENROLLED

        user_status_types = [
            UserStatusType(name=DISABLED),
            UserStatusType(name=ACTIVE),
            UserStatusType(name=SUSPENDED),
            UserStatusType(name=ENROLLED),
            UserStatusType(name=DISENROLLED),
        ]
        db.session.add_all(user_status_types)
        db.session.commit()

    def seed_otp_data(self, id):
        from model.user_otp import UserOTPModel

        otp = UserOTPModel(user_id=id, otp="3232")
        db.session.add(otp)
        db.session.commit()
        return otp

    def seed_auth_token_data(self, id):
        from model.authentication_token import AuthenticationToken

        auth = AuthenticationToken(registration_id=id, key="dse123")
        db.session.add(auth)
        db.session.commit()
        return auth

    def assign_role(self, uid, rid):
        from model.user_roles import UserRoles

        user_role = UserRoles(role_id=rid, user_id=uid)
        db.session.add(user_role)
        db.session.commit()
        return user_role

    def provider_role_types(self):
        provider_role = [
            ProviderRoleTypes(name="prescribing"),
            ProviderRoleTypes(name="outpatient"),
        ]
        db.session.add_all(provider_role)
        db.session.commit()

    def mock_requests_response(self, code, data):
        import requests

        r = requests.Response()
        r.status_code = code
        r.json = data
        return r
