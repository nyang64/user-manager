from model.providers_roles import ProviderRoles


class TestProviderRole:
    def test_base_schema_with_none(self):
        ProviderRoles.id = None
        ProviderRoles.provider_id = None
        ProviderRoles.provider_role_id = None
