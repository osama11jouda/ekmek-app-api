from collections import Counter

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_restful import Resource

from models.item_model import ItemModel
from models.order_model import ItemInOrder, OrderModel
from schemas.order_schema import OrderSchema

order_schema = OrderSchema()


class Order(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        try:
            data = request.get_json()
            user_id = get_jwt_identity()
            items = []
            item_id_quantity = Counter(data['items'])
            for _id, count in item_id_quantity.most_common():
                item = ItemModel.find_item_by_id(_id)
                if not item:
                    return {'msg': 'fail: item not found'}, 404
                items.append(ItemInOrder(item_id=_id, quantity=count))
            order = OrderModel(items=items, user_id=user_id)
            order.save_order()
            return order_schema.dump(order), 200
        except Exception as e:
            return {'msg': f'fail: {str(e)}'}


class UpdateOrder(Resource):
    @classmethod
    @jwt_required()
    def put(cls, order_id):
        try:
            order = OrderModel.find_order_by_id(order_id)
            if not order:
                return {'msg': 'fail: order not fond'}, 404
            for item in order.items:
                item.delete_item_in_order()
            data = request.get_json()
            items = []
            item_id_quantity = Counter(data['items'])
            for _id, count in item_id_quantity.most_common():
                item = ItemModel.find_item_by_id(_id)
                if not item:
                    return {'msg': 'fail: item not found'}, 404
                items.append(ItemInOrder(item_id=_id, quantity=count))
            order.items = items
            order.save_order()
            return order_schema.dump(order), 200
        except Exception as e:
            return {'msg': f'fail: {str(e)}'}


class DeleteOrder(Resource):
    @classmethod
    @jwt_required()
    def delete(cls, order_id):
        try:
            order = OrderModel.find_order_by_id(order_id)
            if not order:
                return {'msg': 'fail: order not fond'}, 404
            for item in order.items:
                item.delete_item_in_order()
            order.delete_order()
            return {'msg': 'success: order deleted'}, 200
        except Exception as e:
            return {'msg': f'fail: {str(e)}'}


class OrderIsPacked(Resource):
    @classmethod
    @jwt_required()
    def get(cls, order_id: int):
        try:
            claim = get_jwt()
            if not claim['is_admin']:
                return {'msg': 'fail: user is not admin'}, 400
            order = OrderModel.find_order_by_id(order_id)
            if not order:
                return {'msg': 'fail: order not fond'}, 404
            order.is_packed = True
            order.save_order()
            return {'msg': 'success: order is packed'}, 200
        except Exception as e:
            return {'msg': f'fail: {str(e)}'}


class OrderIsShipped(Resource):
    @classmethod
    @jwt_required()
    def get(cls, order_id: int):
        try:
            claim = get_jwt()
            if not claim['is_admin']:
                return {'msg': 'fail: user is not admin'}, 400
            order = OrderModel.find_order_by_id(order_id)
            if not order:
                return {'msg': 'fail: order not fond'}, 404
            order.is_shipped = True
            order.save_order()
            return {'msg': 'success: order is shipped'}, 200
        except Exception as e:
            return {'msg': f'fail: {str(e)}'}


class OrderIsDelivered(Resource):
    @classmethod
    @jwt_required()
    def get(cls, order_id: int):
        try:
            claim = get_jwt()
            if not claim['is_admin']:
                return {'msg': 'fail: user is not admin'}, 400
            order = OrderModel.find_order_by_id(order_id)
            if not order:
                return {'msg': 'fail: order not fond'}, 404
            order.is_delivered = True
            order.save_order()
            return {'msg': 'success: order is delivered'}, 200
        except Exception as e:
            return {'msg': f'fail: {str(e)}'}


class UserOrders(Resource):

    @classmethod
    @jwt_required()
    def get(cls):
        try:
            user_id = get_jwt_identity()
            return {'orders': order_schema.dump(OrderModel.find_user_orders(user_id=user_id), many=True)}, 200
        except Exception as e:
            return {'msg': f'fail: {str(e)}'}


class OrdersList(Resource):

    @classmethod
    @jwt_required()
    def get(cls):
        try:
            claim = get_jwt()
            if not claim['is_admin']:
                return {'msg': 'fail: user is not admin'}, 400
            return {'orders': order_schema.dump(OrderModel.find_all(), many=True)}, 200
        except Exception as e:
            return {'msg': f'fail: {str(e)}'}
