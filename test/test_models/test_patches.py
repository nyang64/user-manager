from model.patches import Patches


class TestPatches:
    def test_base_schema_with_none(self):
        Patches.id = None
        Patches.patient_device_id = None
