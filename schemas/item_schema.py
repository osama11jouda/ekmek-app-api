from ma import ma
from models.item_model import ItemModel


class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemModel
        # load_only = ('',)
        dump_only = ('id',)
        load_instance = True
