import pytest
from schema.patient_schema import (
    PatientDetailSchema, must_not_blank, validate_device_serial_number)


class TestClass:
    def test_register_schema_with_none(self):
        with pytest.raises(Exception) as e:
            create_provider = PatientDetailSchema()
            assert create_provider.load('')
        assert "400 Bad Request" in str(e.value)

    def test_validate_device_serial_number_none(self):
        with pytest.raises(Exception) as e:
            assert validate_device_serial_number(None)
        assert "parameter missing" in str(e.value)

    def test_validate_device_serial_number_invalid(self):
        with pytest.raises(Exception) as e:
            assert validate_device_serial_number('1')
        assert "device_serial_number should be of 8 digit only" in str(e.value)

    def test_report_schema_mustnotblank(self):
        with pytest.raises(Exception) as e:
            assert must_not_blank('')
        assert "parameter is missing" in str(e.value)
