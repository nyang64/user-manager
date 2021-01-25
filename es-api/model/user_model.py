from db import db
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import backref


class UserModel(db.Model):
    __tablename__ = "users"
    __table_args__ = ({"schema": "ES"})
    id = db.Column(Integer, primary_key=True)
    username = db.Column('username', String(50), nullable=False, unique=True)
    password = db.Column('password', String(100), nullable=False)
    type_id = db.Column('type_id', Integer, ForeignKey('ES.user_type.id'))
    user_type = db.relationship(
        "UserType", backref=backref("user_type")
    )
    status_id = db.Column('status_id', Integer, ForeignKey('ES.status.id'))
    user_status = db.relationship(
        "UserStatus", backref=backref("user_status")
    )
    scope_id = db.Column('scope_id', Integer, ForeignKey('ES.scope.id'))
    user_scope = db.relationship(
        "UserScope", backref=backref("user_scope")
    )

    def __init__(self, username, password, user_type, user_status, user_scope):
        self.username = username
        self.password = password
        self.type_id = user_type
        self.status_id = user_status
        self.scope_id = user_scope
        # self.user_type = user_type
        # self.user_status = user_status
        # self.user_scope = user_scope

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def update_db(self) -> None:
        db.session.commit()