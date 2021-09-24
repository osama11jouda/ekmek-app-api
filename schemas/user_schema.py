from ma import ma
from models.user_model import UserModel
from schemas.address_schema import AddressSchema


class UserSchema(ma.SQLAlchemyAutoSchema):
    address = ma.Nested(AddressSchema, many=True)

    class Meta:
        model = UserModel
        load_only = ('password',)
        dump_only = ('id',)
        include_fk = True
        load_instance = True
