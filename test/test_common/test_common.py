from config import read_environ_value
from utils import common
from utils.common import toJson
from utils.common import MyEncoder
from utils.common import auth_response_model
import pytest
from werkzeug.exceptions import BadRequest


class TestCommon:
    def test_read_environ_blank(self):
        print(read_environ_value(
            '{\'POSTGRES_DB_PORT\':None}', 'POSTGRES_DB_PORT'))

    def test_encPass(self):
        resp = common.encPass('Avilash')
        assert resp is not None
        pswd = common.checkPass('Avilash', resp)
        assert pswd is True
        pswd = common.checkPass('Avilash1', resp)
        assert pswd is False

    def test_to_json_class(self):
        with pytest.raises(AttributeError) as e:
            toJson().default({'Avilash': 'Av'})
        assert type(e.value) is AttributeError

    def test_my_encoder_class(self):
        with pytest.raises(AttributeError) as e:
            MyEncoder().default({'Avilash': 'Av'})
        assert type(e.value) is AttributeError

    def test_generateOTP_uuid(self):
        otp = common.generateOTP()
        assert otp is not None
        ud = common.generate_uuid()
        assert ud is not None

    def test_have_keys_NotForce(self):
        rsp = common.have_keys_NotForce({'AB': 'V'}, ('A'))
        assert rsp is False
        rsp = common.have_keys_NotForce('', ('A'))
        assert rsp is False
        rsp = common.have_keys_NotForce({'A': 'value'}, ('A'))
        assert rsp is True

    def test_have_keys(self):
        rsp = common.have_keys({'A': 'value'}, ('A'))
        assert rsp is True
        with pytest.raises(BadRequest) as e:
            rsp = common.have_keys({'AB': 'V'}, ('A'))
            assert rsp is False
            rsp = common.have_keys('', ('A'))
            assert rsp is False
        assert type(e.value) is BadRequest

    def test_token_time(self):
        resp = common.tokenTime(False)
        assert resp is not None
        resp = common.tokenTime(True)
        assert resp is not None

    def test_auth_response_model(self):
        resp = auth_response_model(id_token='Token', message='Msg')
        assert resp is not None

    def test_time_diff(self):
        from datetime import datetime
        resp = common.timeDiff(first_time=datetime.now(),
                               second_time=datetime.now())
        assert resp is not None
