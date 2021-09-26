from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api
from marshmallow import ValidationError
from flask_uploads import configure_uploads, patch_request_class

from libs.image_helper import IMAGE_SET
from models.blocklist_model import BlockListModel
from resources.address import UserAddress, AddressList
from resources.image import UserAvatar, DeleteAvatarImage, ItemImage, DeleteItemImage
from resources.item import RegisterItem, ItemList, UpdateItem, DeleteItem
from resources.order import Order, OrdersList, UpdateOrder, DeleteOrder, OrderIsPacked, OrderIsShipped, \
    OrderIsDelivered, UserOrders
from resources.user import RegisterUser, UserLogin, RefreshToken, UserLogout, User, UsersList

app = Flask(__name__)
load_dotenv('.env', verbose=True)
app.config.from_object("default_config")
# app.config.from_envvar("default_config.py")
api = Api(app)
jwt = JWTManager(app)
configure_uploads(app, IMAGE_SET)
patch_request_class(app, 10*1024*1024)


@jwt.additional_claims_loader
def adding_admin_claim(identity):
    admins = (1, 2, 3)
    if identity in admins:
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.token_in_blocklist_loader
def handle_block_jti(_, jwt_payload):
    jti = jwt_payload['jti']
    token = BlockListModel.find_jti(jti)
    return token is not None


@app.errorhandler(ValidationError)
def handle_validation(error):
    return jsonify(error.messages)


# user routes
api.add_resource(RegisterUser, '/user/register')  # post
api.add_resource(UserLogin, '/user/login')  # post
api.add_resource(RefreshToken, '/user/refresh')  # get
api.add_resource(UserLogout, '/user/logout')  # get
api.add_resource(UserAddress, '/user/address')  # post
api.add_resource(User, '/user')  # for getting user data & updating user data (get , put)
api.add_resource(UserAvatar, '/user/avatar')  # post
api.add_resource(DeleteAvatarImage, '/user/avatar/delete/<string:path>')  # delete
api.add_resource(Order, '/user/order')  # post
api.add_resource(UpdateOrder, '/user/order/update/<int:order_id>')  # put
api.add_resource(DeleteOrder, '/user/order/delete/<int:order_id>')  # delete
api.add_resource(UserOrders, '/user/orders')  # get


# admin routes
api.add_resource(RegisterItem, '/admin/item/register')  # post
api.add_resource(UpdateItem, '/admin/item/update/<int:item_id>')  # put
api.add_resource(DeleteItem, '/admin/item/delete/<int:item_id>')  # delete
api.add_resource(ItemImage, '/admin/item/image/<int:item_id>')  # post
api.add_resource(DeleteItemImage, '/admin/image/delete/<int:item_id>/<string:img_name>')  # delete
api.add_resource(UsersList, '/admin/users')  # get
api.add_resource(AddressList, '/admin/users/addresses')  # get
api.add_resource(ItemList, '/admin/items')  # get
api.add_resource(OrdersList, '/admin/orders')  # get
api.add_resource(OrderIsPacked, '/admin/order/packed/<int:order_id>')  # get
api.add_resource(OrderIsShipped, '/admin/order/shipped/<int:order_id>')  # get
api.add_resource(OrderIsDelivered, '/admin/order/delivered/<int:order_id>')  # get


# if __name__ == '__main__':
app.run(port=5000)
