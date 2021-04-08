import pytest
from schema.facility_schema import AddFacilitySchema
from unittest import TestCase
from werkzeug.exceptions import BadRequest


class TestFacilitySchema(TestCase):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    def test_add_facility_schema(self):
        args = {"facility_name": "FCAJ",
                "address": {
                    "street_address_1": "Test",
                    "street_address_2": "Te",
                    "city": "Kyn",
                    "state": "MH",
                    "country": "IN",
                    "postal_code": "421306"
                }}
        user_role = AddFacilitySchema().load(args)
        print(user_role, type(user_role))
        self.assertIsInstance(user_role, tuple)

    def test_add_facility_schema_raise_exception(self):
        with pytest.raises(BadRequest) as e:
            AddFacilitySchema().load('')
        print(str(e.value))
        self.assertIsInstance(e.value, BadRequest)
        self.assertIn('_schema', str(e.value))
        self.assertIn('Invalid input', str(e.value))

    def test_add_facility_schema_none_value(self):
        with pytest.raises(BadRequest) as e:
            AddFacilitySchema().load({'facility_name': ''})
        print(str(e.value))
        self.assertIsInstance(e.value, BadRequest)
        self.assertIn('parameter is missing', str(e.value))
