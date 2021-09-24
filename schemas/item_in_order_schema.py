from ma import ma
from models.order_model import ItemInOrder


class ItemInOrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemInOrder
        include_fk = True
        load_instance = True
