from ma import ma
from model.address import Address


class AddressSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Address
        load_instance = True

    id = ma.auto_field(dump_only=True)
