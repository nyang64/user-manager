# generate_signed_url

import datetime

import pytest
from utils.common import (
    generate_signed_url,
    have_keys,
    is_json,
    responseModel,
    timeDiff,
)


class TestCommonUtils:
    def test_is_json_none_data(self):
        with pytest.raises(Exception) as e:
            assert is_json(None)
        assert "400 Bad Request" in str(e.value)

    def test_have_keys_none_data(self):
        with pytest.raises(Exception) as e:
            assert have_keys(None, None)
        assert "400 Bad Request" in str(e.value)

    def test_generate_signed_url_none_data(self):
        with pytest.raises(Exception) as e:
            assert generate_signed_url(None)
        assert "expected string or bytes-like object" in str(e.value)

    def test_generate_signed_url_none_invalid_data(self):
        with pytest.raises(Exception) as e:
            assert generate_signed_url("")
        assert "expected string or bytes-like object" in str(e.value)

    def test_time_differance_none_invalid_data(self):
        with pytest.raises(Exception) as e:
            assert timeDiff(datetime.datetime, datetime.datetime)
        assert "unsupported operand type" in str(e.value)

    def test_response_model_invalid_data(self):
        responseModel(None, None, None)
