import logging
import uuid

from db import db
from model.base_model import BaseModel
from model.user_registration import UserRegister
from model.user_roles import UserRoles
from model.user_status import UserStatus
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.exceptions import InternalServerError, NotFound

# "UserRoles" model is required so that the ORM
# can make the 'roles' 'relationship'


class Users(BaseModel):
    __tablename__ = "users"
    __table_args__ = {"schema": "ES"}
    registration_id = db.Column(
        "registration_id",
        Integer,
        ForeignKey("ES.registrations.id", ondelete="CASCADE"),
    )
    first_name = db.Column("first_name", String(30), nullable=False)
    last_name = db.Column("last_name", String(30), nullable=False)
    phone_number = db.Column("phone_number", String(12), nullable=False)
    uuid = db.Column(
        UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False
    )
    external_user_id = db.Column("external_user_id", String(10), nullable=True)
    registration = db.relationship("UserRegister", backref="registrations")
    roles = db.relationship("UserRoles", lazy="joined", uselist=True)
    statuses = db.relationship(
        "UserStatus", order_by="desc(UserStatus.created_at)", lazy="dynamic"
    )

    @classmethod
    def all(cls) -> "Users":
        return cls.query.all()

    @classmethod
    def find_by_email(cls, email: str) -> "Users":
        user_registration = UserRegister.find_by_email(email)
        return cls.find_by_registration_id(user_registration.id)

    @classmethod
    def find_by_registration_id(cls, registration_id: str) -> "Users":
        return cls.query.filter_by(registration_id=registration_id).first()

    @classmethod
    def find_by_id(cls, _id: str) -> "Users":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_patient_id(cls, patient_id: str) -> "Users":
        return cls.query.filter_by(id=patient_id).first()

    @classmethod
    def check_user_exist(cls, user_id):
        return db.session.query(cls).filter_by(id=user_id).first()

    @classmethod
    def get_user_by_registration_id(cls, user_reg_id):
        try:
            user = cls.find_by_registration_id(registration_id=user_reg_id)
            if user is None:
                raise NotFound("User Details Not Found")
            return user
        except Exception as e:
            logging.error(e)
            raise InternalServerError("Something Went Wrong")

    def status(self):
        return self.statuses.limit(1)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
