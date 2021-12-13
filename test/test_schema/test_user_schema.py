import pytest
from schema.user_schema import must_not_blank


class TestUserSchema:
    def test_report_schema_mustnotblank(self):
        with pytest.raises(Exception) as e:
            assert must_not_blank("")
        assert "parameter is missing" in str(e.value)
