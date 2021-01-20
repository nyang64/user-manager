from db import db
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import backref


class ES_Users(db.Model):
    __tablename__ = "es_users"
    __table_args__ = ({"schema": "ES"})
    id = db.Column(Integer, primary_key=True)
    first_name = db.Column(String(30))
    last_name = db.Column(String(30))
    phone = db.Column(String(12))
    email = db.Column(String(50))
    address = db.Column(Integer)
    scope = db.Column(Integer)
    user_id = db.Column(Integer, ForeignKey('ES.users.id'))
    UserID = db.relationship(
        "UserModel", backref=backref("users", uselist=False)
    )

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
