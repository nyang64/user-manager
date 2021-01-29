from model.user_registration import UserRegister
from model.user_scope import UserScope
from model.user_type import UserType
from model.user_status import UserStatus
from marshmallow_sqlalchemy import ModelSchema


class UserType(ModelSchema):
    class Meta:
        model = UserType
        dump_only = ("id",)
        include_fk = True


class UserStatus(ModelSchema):
    class Meta:
        model = UserStatus
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
