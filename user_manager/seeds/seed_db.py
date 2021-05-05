import os

from flask_seeder import Seeder
from seeds import admins, device, patients, providers, roles, user_status_types


class SeedDemo(Seeder):
    def run(self):
        print("seeding db")
        # device.seed()
        # roles.seed()
        user_status_types.seed()
        # admins.seed()
        # if os.environ.get("FLASK_ENV") != "production":
        #     created_providers = providers.seed()
        #     patients.seed(created_providers["outpatient"], created_providers["prescribing"])
