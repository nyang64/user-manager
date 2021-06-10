from unittest import TestCase

import pytest
from marshmallow import ValidationError
from model.provider_role_types import ProviderRoleTypes
from schema.provider_role_types_schema import ProviderRoleTypesSchema


class TestProviderRoleTypesSchema(TestCase):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    def test_provider_role_type_schema(self):
        args = {"name": "Avilash"}
        provider_role = ProviderRoleTypesSchema().load(args)
        self.assertIsInstance(provider_role, ProviderRoleTypes)

    def test_provider_role_schema_raise_exception(self):
        with pytest.raises(ValidationError) as e:
            ProviderRoleTypesSchema().load("")
        print(str(e.value))
        self.assertIsInstance(e.value, ValidationError)
        self.assertIn("_schema", str(e.value))
        self.assertIn("Invalid input", str(e.value))
