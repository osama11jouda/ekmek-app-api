from flask import request
from flask_jwt_extended import jwt_required, get_jwt
from flask_restful import Resource

from models.item_model import ItemModel
from schemas.item_schema import ItemSchema

item_schema = ItemSchema()


class RegisterItem(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        claim = get_jwt()
        if not claim['is_admin']:
            return {'msg': 'user not admin'}, 400
        data = request.get_json()
        item_data = item_schema.load(data)
        item = ItemModel.find_item_by_name(item_data.name)
        if item:
            return {'msg': 'fail: item with same name already exists'}, 400
        item_data.save_item()
        return item_schema.dump(item_data), 201


class UpdateItem(Resource):
    @classmethod
    @jwt_required()
    def put(cls, item_id: int):
        claim = get_jwt()
        if not claim['is_admin']:
            return {'msg': 'user not admin'}, 400
        item = ItemModel.find_item_by_id(item_id)
        if not item:
            return {'msg': 'fail: item not found'}, 404
        data = request.get_json()
        item_data = item_schema.load(data, partial=('name', 'price', 'desc'))
        if item_data.name:
            item.name = item_data.name
        if item_data.price:
            item.price = item_data.price
        if item_data.desc:
            item.desc = item_data.desc
        item.save_item()
        return item_schema.dump(item), 200


class DeleteItem(Resource):
    @classmethod
    @jwt_required()
    def delete(cls, item_id: int):
        claim = get_jwt()
        if not claim['is_admin']:
            return {'msg': 'user not admin'}, 400
        item = ItemModel.find_item_by_id(item_id)
        if not item:
            return {'msg': 'fail: item not found'}, 404
        item.delete_item()
        return {'msg': 'success: item deleted'}, 200


class ItemList(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        claim = get_jwt()
        if not claim['is_admin']:
            return {'msg': 'user not admin'}, 400
        return {'items': item_schema.dump(ItemModel.find_all(), many=True)}
