from db import db
from sqlalchemy import Integer, ForeignKey
from model.base_model import BaseModel


class ProviderRoles(BaseModel):
    __tablename__ = "providers_roles"
    __table_args__ = ({"schema": "ES"})
    provider_role_id = db.Column('provider_role_id',
                                 Integer,
                                 ForeignKey('ES.provider_role_types.id',
                                            ondelete="CASCADE"))
    provider_id = db.Column('provider_id',
                            Integer,
                            ForeignKey('ES.providers.id',
                                       ondelete="CASCADE"))
    @classmethod
    def all(cls) -> "ProviderRoles":
        return cls.query.all()

    @classmethod
    def find_by_provider_id(cls, _provider_id):
        return cls.query.filter_by(provider_id=_provider_id).all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
