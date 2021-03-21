from model.address import Address
from ma import ma


class AddressSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Address
        load_instance = True

    id = ma.auto_field(dump_only=True)
    user_id = ma.auto_field()
