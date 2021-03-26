from model.user_roles import UserRoles
from ma import ma


class UserRolesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserRoles
        load_instance = True

    id = ma.auto_field(dump_only=True)
    user_id = ma.auto_field()
    role_id = ma.auto_field()
