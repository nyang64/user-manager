from ma import ma
from model.roles import Roles


class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Roles
        load_instance = True

    id = ma.auto_field(dump_only=True)
