from model.patches import Patches


class TestClass:
    def test_base_schema_with_none(self):
        Patches.id = None
        Patches.patient_device_id = None
