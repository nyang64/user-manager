import pytest
import json

from schema.material_request_schema import (
    MaterialListSchema,
    must_not_blank,
    add_materials_schema,
    AddMaterialSchema
)

class TestMaterialRequestSchema:
    def test_add_material_request_schema_with_none(self):
        with pytest.raises(Exception) as e:
            material_request = AddMaterialSchema()
            assert material_request.load("")
        assert "400 Bad Request" in str(e.value)


