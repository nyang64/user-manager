from db import db
from model.base_model import BaseModel
from sqlalchemy import Sequence

# define sequence explicitly
MATERIAL_REQ_SEQUENCE = Sequence('material_req_seq', start=100000, increment=1, schema="ES")


class MaterialRequests(BaseModel):
    __tablename__ = "material_requests"
    __table_args__ = {"schema": "ES"}

    request_number = db.Column("request_number", db.Integer, MATERIAL_REQ_SEQUENCE,
                               server_default=MATERIAL_REQ_SEQUENCE.next_value())
    num_items = db.Column("num_items", db.Integer, nullable=False, default=0)
    request_date = db.Column("request_date", db.DateTime)
    requested_user_id = db.Column("requested_user", db.Integer,
                                  db.ForeignKey("ES.users.id", ondelete="CASCADE"), nullable=False)
    request_log_location = db.Column("request_log_location", db.String(200))

    @classmethod
    def all(cls) -> "MaterialRequests":
        return cls.query.all()

    @classmethod
    def all_records(cls) -> "MaterialRequests":
        return db.session.query(cls).all()

    @classmethod
    def find_by_id(cls, _id: str) -> "MaterialRequests":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_user_id(cls, _request_number) -> "MaterialRequests":
        return cls.query.filter_by(request_number=_request_number).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        db.session.flush()
        db.session.refresh(self)
        print(self)
        return self
