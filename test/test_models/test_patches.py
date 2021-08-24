from model.patients_patches import PatientsPatches


class TestPatches:
    def test_base_schema_with_none(self):
        PatientsPatches.id = None
        PatientsPatches.patient_device_id = None
