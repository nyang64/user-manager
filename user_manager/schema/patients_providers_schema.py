from ma import ma
from model.patients_providers import PatientsProviders


class PatientsProvidersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PatientsProviders
        load_instance = True

    id = ma.auto_field(dump_only=True)
    patient_id = ma.auto_field()
    provider_id = ma.auto_field()
    provider_role_id = ma.auto_field()
