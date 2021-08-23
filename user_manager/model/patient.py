from db import db
from model.base_model import BaseModel


class Patient(BaseModel):
    __tablename__ = "patients"
    __table_args__ = {"schema": "ES"}
    user_id = db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("ES.users.id", ondelete="CASCADE"),
        nullable=False,
    )
    emergency_contact_name = db.Column(
        "emergency_contact_name", db.String(30), nullable=False
    )
    emergency_contact_number = db.Column(
        "emergency_contact_phone", db.String(12), nullable=False
    )
    gender = db.Column("gender", db.String(12))
    date_of_birth = db.Column("date_of_birth", db.String(30), nullable=False)
    enrolled_date = db.Column("enrolled_at", db.DateTime, default=db.func.now())
    gender = db.Column("gender", db.String(30), nullable=False)
    indication = db.Column("indication", db.String(40), nullable=False)
    address_id = db.Column(
        "address_id",
        db.Integer,
        db.ForeignKey("ES.addresses.id", ondelete="CASCADE"),
        nullable=True,
    )
    mobile_app_user = db.Column("mobile_app_user", db.Boolean, default=True)
    address = db.relationship(
        "Address", backref="address", uselist=False, viewonly=True
    )
    user = db.relationship("Users", backref="users", uselist=False, viewonly=True)
    devices = db.relationship(
        "PatientsDevices", backref="patients_id", uselist=True, viewonly=True
    )

    @classmethod
    def all(cls) -> "Patient":
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id):
        return db.session.query(cls).filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
