from model.patients_providers import PatientsProviders


class TestPatientProvider:
    def test_base_schema_with_none(self):
        PatientsProviders.id = None
        PatientsProviders.patient_id = None
        PatientsProviders.provider_id = None
        PatientsProviders.provider_role_id = None
