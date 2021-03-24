from flask_seeder import Seeder
from seeds import roles
from seeds import patients
from seeds import providers
from model.providers import Providers
from seeds.admin_manager import AdminManager
import os

class SeedDemo(Seeder):
    def run(self):
        print('seeding db')

        # Create an admin user irrespective of the env
        admin = AdminManager()
        result = admin.seed_db()

        if os.environ.get("FLASK_ENV") != "production":
            result = self.seed_dev()

        print('Status', result)

    # def seed_admin(self):
    #     provider = ADMIN_USER["provider"]
    #     facility = provider["facility"]
    #     facility_address = facility["address"]
    #
    #     roles.seed()
    #     patients.seed()
    #
    #     self.create_and_register_user(provider)
    #     address_id = facility_obj.save_address(facility_address)
    #     facility_obj.save_facility(facility["name"], address_id)
    #     self.print_message_details()

        # return True


    def seed_dev(self):
        roles.seed()

        admin = AdminManager()
        result = admin.seed_db()
        outpatient = Providers.find_by_id(1)
        prescribing = Providers.find_by_id(2)
        patients.seed(outpatient, prescribing)
