from ma import ma
from model.user_status_type import UserStatusType


class UserStatusTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserStatusType
        load_instance = True

    id = ma.auto_field(dump_only=True)
