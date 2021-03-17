from model.provider_role_types import ProviderRoleTypes


class TestPatientProviderRole:
    def test_base_schema_with_none(self):
        ProviderRoleTypes.id = None
        ProviderRoleTypes.name = None
        ProviderRoleTypes.updated_on = None
