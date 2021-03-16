import pytest
from schema.update_password_schema import UserUpdateSchema


class TestClass:

    def test_update_password_schema_mustnotblank(self):
        with pytest.raises(Exception) as e:
            assert UserUpdateSchema.must_not_blank('')
        assert "cannot be null" in str(e.value)

    def test_update_password_schema(self):
        with pytest.raises(Exception) as e:
            assert UserUpdateSchema.validate_data('')
        assert "400 Bad Request" in str(e.value)
