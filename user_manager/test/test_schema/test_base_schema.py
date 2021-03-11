import pytest
from schema.base_schema import validate_number


class TestClass:
    def test_base_schema_with_none(self):
        with pytest.raises(Exception) as e:
            assert validate_number(None)
        assert "phone_number cannot be None" in str(e.value)

    def test_base_schema_with_non_numeric(self):
        with pytest.raises(Exception) as e:
            assert validate_number('abc')
        assert "phone_number should be numeric" in str(e.value)

    def test_base_schema_with_invalid_phone(self):
        with pytest.raises(Exception) as e:
            assert validate_number('1234')
        assert "Number less than 10 digit" in str(e.value)
