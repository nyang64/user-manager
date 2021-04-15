from flask_seeder import Seeder
from seeds import roles
from seeds import patients
from seeds import providers
from seeds import admins
from seeds import device

import os


class SeedDemo(Seeder):
    def run(self):
        print('seeding db')
        device.seed()
        roles.seed()
        admins.seed()
        if os.environ.get("FLASK_ENV") != "production":
            created_providers = providers.seed()
            patients.seed(created_providers["outpatient"], created_providers["prescribing"])
