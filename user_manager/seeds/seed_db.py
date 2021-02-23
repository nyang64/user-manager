from flask_seeder import Seeder
from seeds.admin_manager import AdminManager


class SeedDemo(Seeder):
    def run(self):
        print('seeding db')
        admin = AdminManager()
        result = admin.seed_db()
        print('Status', result)
