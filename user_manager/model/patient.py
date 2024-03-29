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
    emergency_contact_relationship = db.Column(
        "emergency_contact_relationship", db.String(30), nullable=True
    )
    gender = db.Column("gender", db.String(12))
    date_of_birth = db.Column("date_of_birth", db.String(30), nullable=False)
    enrolled_date = db.Column("enrolled_at", db.DateTime, default=db.func.now())
    unenrolled_at = db.Column("unenrolled_at", db.DateTime, nullable=True)
    gender = db.Column("gender", db.String(30), nullable=False)
    indication = db.Column("indication", db.String(40), nullable=False)
    permanent_address_id = db.Column(
        "permanent_address_id",
        db.Integer,
        db.ForeignKey("ES.addresses.id", ondelete="CASCADE"),
        nullable=True,
    )
    mobile_app_user = db.Column("mobile_app_user", db.Boolean, default=True)
    shipping_address_id = db.Column(
        "shipping_address_id",
        db.Integer,
        db.ForeignKey("ES.addresses.id", ondelete="CASCADE"),
        nullable=True
    )
    permanent_address = db.relationship(
        "Address", foreign_keys=[permanent_address_id]
    )
    shipping_address = db.relationship(
        "Address", foreign_keys=[shipping_address_id]
    )
    user = db.relationship("Users", backref="users", uselist=False, viewonly=True)
    devices = db.relationship(
        "PatientsDevices", backref="patients_id", uselist=True, viewonly=True
    )
    patches = db.relationship("PatientsPatches", backref="patients_id",
                              uselist=True, viewonly=True)

    patient_details = db.relationship("PatientDetails", backref="patients_id",
                                      uselist=True, viewonly=True)

    @classmethod
    def all(cls) -> "Patient":
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id):
        return db.session.query(cls).filter_by(id=_id).first()

    @classmethod
    def find_by_user_id(cls, _user_id):
        return db.session.query(cls).filter_by(user_id=_user_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def copy(self, updated_obj):
        self.emergency_contact_name = updated_obj.emergency_contact_name
        self.emergency_contact_number = updated_obj.emergency_contact_number
        self.date_of_birth = updated_obj.date_of_birth
        self.enrolled_date = updated_obj.enrolled_date
        self.gender = updated_obj.gender
        self.indication = updated_obj.indication
        self.mobile_app_user = updated_obj.mobile_app_user

