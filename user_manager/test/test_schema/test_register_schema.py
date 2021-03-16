import pytest
from schema.register_schema import (
    RegisterSchema, must_not_blank, register_schema)


class TestClass:
    def test_register_schema_with_none(self):
        with pytest.raises(Exception) as e:
            create_provider = RegisterSchema()
            assert create_provider.load('')
        assert "400 Bad Request" in str(e.value)

    def test_register_schema_with_none_data(self):
        with pytest.raises(Exception) as e:
            assert register_schema.load(None)
        assert "400 Bad Request" in str(e.value)

    def test_register_schema_with_data(self):
        with pytest.raises(Exception) as e:
            assert register_schema.load(
                {
                    'email': '',
                    'password': ''
                })
        assert "400 Bad Request" in str(e.value)

    def test_report_schema_mustnotblank(self):
        with pytest.raises(Exception) as e:
            assert must_not_blank('')
        assert "parameter is missing" in str(e.value)
