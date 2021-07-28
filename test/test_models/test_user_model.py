import pytest
from model.users import Users


class TestUserModel:
    def test_base_schema_with_none(self):
        with pytest.raises(Exception) as e:
            assert Users.get_user_by_registration_id(None)
        assert "500 Internal Server Error" in str(e.value)
