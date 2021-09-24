from ma import ma
from models.address_model import AddressModel


class AddressSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AddressModel
        # load_only = ('',)
        dump_only = ('id',)
        include_fk = True
        load_instance = True
