from ma import ma
from model.provider_role_types import ProviderRoleTypes


class ProviderRoleTypesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProviderRoleTypes
        load_instance = True

    id = ma.auto_field(dump_only=True)
