import pytest
from schema.report_schema import report_id_schema, must_not_blank


class TestReportSchema:
    def test_report_schema_with_none(self):
        with pytest.raises(Exception) as e:
            assert report_id_schema.load(None)
        assert "400 Bad Request" in str(e.value)

    def test_report_schema_with_blank(self):
        with pytest.raises(Exception) as e:
            assert report_id_schema.load('')
        assert "400 Bad Request" in str(e.value)

    def test_report_schema_mustnotblank(self):
        with pytest.raises(Exception) as e:
            assert must_not_blank('')
        assert "parameter is missing" in str(e.value)
