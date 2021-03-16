import pytest
from schema.provider_schema import (
    CreateProviderSchema, UpdateProviderSchema, must_not_blank)


class TestClass:
    def test_create_provider_schema_with_none(self):
        with pytest.raises(Exception) as e:
            create_provider = CreateProviderSchema()
            assert create_provider.load('')
        assert "400 Bad Request" in str(e.value)

    def test_update_provider_schema_with_blank(self):
        with pytest.raises(Exception) as e:
            assert UpdateProviderSchema.load('')
        assert "400 Bad Request" in str(e.value)

    def test_report_schema_mustnotblank(self):
        with pytest.raises(Exception) as e:
            assert must_not_blank('')
        assert "parameter is missing" in str(e.value)
