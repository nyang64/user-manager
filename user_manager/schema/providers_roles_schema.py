from ma import ma
from model.providers_roles import ProviderRoles


class ProvidersRolesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProviderRoles
        load_instance = True

    id = ma.auto_field(dump_only=True)
    provider_role_id = ma.auto_field()
    provider_id = ma.auto_field()
