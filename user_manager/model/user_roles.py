from db import db
from model.base_model import BaseModel
from model.roles import Roles

# the "Roles" model is required so that the ORM
# can make the 'role' 'relationship'


class UserRoles(BaseModel):
    __tablename__ = "user_roles"
    __table_args__ = {"schema": "ES"}
    role_id = db.Column(
        "role_id",
        db.Integer,
        db.ForeignKey("ES.role_types.id", ondelete="CA SCADE"),
        nullable=False,
    )
    user_id = db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("ES.users.id", ondelete="CASCADE"),
        nullable=False,
    )
    role = db.relationship("Roles", backref="roles", uselist=False)

    @classmethod
    def find_by_user_id(cls, user_id: str) -> "UserRoles":
        user_role = cls.query.filter_by(user_id=user_id).first()
        return user_role

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
