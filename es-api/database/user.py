from model.user_registration import UserRegister
from model.user_scope import UserScope
from model.user_status_types import UserStatusType
from marshmallow_sqlalchemy import ModelSchema


class UserStatus(ModelSchema):
    class Meta:
        model = UserStatusType
        dump_only = ("id",)
        include_fk = True


class UserScope(ModelSchema):
    class Meta:
        model = UserScope
        dump_only = ("id",)
        include_fk = True


class UserSchema(ModelSchema):
    class Meta:
        model = UserRegister
        dump_only = ("id",)
        include_fk = True
