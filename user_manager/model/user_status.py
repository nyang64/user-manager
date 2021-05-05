from db import db
from model.base_model import BaseModel
from model.user_status_type import UserStatusType

# the "UserStatusType" model is required so that the ORM
# can make the 'status' 'relationship'


class UserStatus(BaseModel):
    __tablename__ = "user_statuses"
    __table_args__ = {"schema": "ES"}
    status_id = db.Column(
        "status_id",
        db.Integer,
        db.ForeignKey("ES.user_status_types.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id = db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("ES.users.id", ondelete="CASCADE"),
        nullable=False,
    )
    status = db.relationship(
        "UserStatusType", backref="user_status_types", uselist=False
    )
