from model.authentication_token import AuthenticationToken


class TestClass:
    def test_base_schema_with_none(self):
        auth = AuthenticationToken()
        auth.registration_id = None
        auth.key = None
