from utils.validation import validate_number, get_param, validate_request
import pytest


class TestClass:
    def test_validate_number_none(self):
        with pytest.raises(Exception) as e:
            assert validate_number(None)
        assert "400 Bad Request" in str(e.value)

    def test_validate_number_not_valid(self):
        with pytest.raises(Exception) as e:
            assert validate_number('1')
        assert "400 Bad Request" in str(e.value)

    def test_validate_number_alphabetic(self):
        with pytest.raises(Exception) as e:
            assert validate_number('abc')
        assert "400 Bad Request" in str(e.value)

    def test_validate_number_valid(self):
        validate_number('1111111111')

    def test_validate_request_none(self):
        with pytest.raises(Exception) as e:
            assert get_param(None, None)
        assert "NoneType' is not iterable" in str(e.value)

    def test_validate_request_valid(self):
        with pytest.raises(Exception) as e:
            get_param('a', 'a,b,c')
        assert "no attribute 'get'" in str(e.value)

    def test_validate_request_valid_but_not(self):
        with pytest.raises(Exception) as e:
            assert get_param('x', 'a,b,c')
        assert "400 Bad Request" in str(e.value)

    def test_validate_request_json(self):
        with pytest.raises(Exception) as e:
            assert validate_request()
        assert "Working outside of request context" in str(e.value)
