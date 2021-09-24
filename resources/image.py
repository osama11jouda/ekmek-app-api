import os
import uuid
from time import time

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_restful import Resource
from flask_uploads import UploadNotAllowed

from libs.image_helper import save_image
from models.item_model import ItemModel
from models.user_model import UserModel
from schemas.image_schema import ImageSchema

image_schema = ImageSchema()


class UserAvatar(Resource):

    @classmethod
    @jwt_required()
    def post(cls):
        image_data = image_schema.load(request.files)
        try:
            user_id = get_jwt_identity()
            folder = f"user_{user_id}"
            image_path = save_image(image_data['image'], folder=folder, name="avatar.")
            user = UserModel.find_user_by_id(user_id)
            if user:
                user.user_image = image_path
                user.save_user()
                return {'msg': 'success: image uploaded'}, 201
            os.unlink('static/images/'+image_path)
            return {'msg': 'fail: user not found'}, 404
        except UploadNotAllowed:
            return {'msg': 'fail: upload not allowed'}, 400
        except Exception as e:
            return {'msg': f'fail:{str(e)}'}

    @jwt_required()
    def put(self, path: str):
        pass


class ItemImage(Resource):
    @jwt_required()
    def post(self, item_id):
        claim = get_jwt()
        if not claim['is_admin']:
            return {'msg': 'fail: user is not admin'}, 400
        image_data = image_schema.load(request.files)
        try:
            item = ItemModel.find_item_by_id(item_id)
            if not item:
                return {'msg': 'fail: item not found'}, 404
            folder = f"items/item_{item.id}"
            name = f"{uuid.uuid4().hex}_{int(time())}."
            image_path = save_image(image_data['image'], folder=folder, name=name)
            item.image = image_path
            item.save_item()
            return {'msg': 'success: image uploaded'}, 201
        except UploadNotAllowed:
            return {'msg': 'fail: upload not allowed'}, 400
        except Exception as e:
            return {'msg': f'fail:{str(e)}'}

    @jwt_required()
    def put(self, path: str):
        pass


class DeleteAvatarImage(Resource):

    @jwt_required()
    def delete(self, path: str):
        user_id = get_jwt_identity()
        user = UserModel.find_user_by_id(user_id)
        print()
        image_path = f'static/images/user_{user_id}/{path}'
        try:
            os.unlink(image_path)
            user.user_image = None
            user.save_user()
            return {'msg': 'image deleted'}, 200
        except Exception as e:
            return {'msg': f'fail: {str(e)}'}


class DeleteItemImage(Resource):

    @classmethod
    @jwt_required()
    def delete(cls, item_id: int,  img_name: str):
        claim = get_jwt()
        if not claim['is_admin']:
            return {'msg': 'fail: user not admin'}, 400
        item = ItemModel.find_item_by_id(item_id)
        if not item:
            return {'msg': 'fail: item not found'}, 404
        image_path = f'static/images/items/item_{item_id}/{img_name}'
        try:
            os.unlink(image_path)
            item.image = None
            item.save_item()
            return {'msg': 'image deleted'}, 200
        except Exception as e:
            return {'msg': f'fail: {str(e)}'}
