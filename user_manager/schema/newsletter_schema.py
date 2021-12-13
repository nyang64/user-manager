import logging

from ma import ma
from model.newsletters import Newsletters


class NewsletterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Newsletters
        load_instance = True

    id = ma.auto_field(dump_only=True)
    user_id = ma.auto_field()
    day_at = ma.auto_field()