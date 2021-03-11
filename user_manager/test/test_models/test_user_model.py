import pytest
from model.users import Users


class TestClass:
    def test_base_schema_with_none(self):
        with pytest.raises(Exception) as e:
            assert Users.getUserById(None)
        assert "500 Internal Server Error" in str(e.value)
