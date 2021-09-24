from ma import ma
from models.order_model import OrderModel
from schemas.item_in_order_schema import ItemInOrderSchema


class OrderSchema(ma.SQLAlchemyAutoSchema):
    items = ma.Nested(ItemInOrderSchema, many=True)

    class Meta:
        model = OrderModel
        dump_only = ('id', 'status')
        include_fk = True
        load_instance = True
