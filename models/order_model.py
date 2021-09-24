from typing import List

from db import db


class ItemInOrder(db.Model):
    __tablename__ = "item_in_order"

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    quantity = db.Column(db.Integer, default=1)

    item = db.relationship("ItemModel")
    order = db.relationship("OrderModel", back_populates="items")

    def delete_item_in_order(self) -> None:
        db.session.delete(self)
        db.session.commit()


class OrderModel(db.Model):
    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    payment = db.Column(db.Boolean, nullable=False, default=False)
    is_packed = db.Column(db.Boolean, nullable=False, default=False)
    is_shipped = db.Column(db.Boolean, nullable=False, default=False)
    is_delivered = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    items = db.relationship("ItemInOrder", lazy="dynamic", back_populates="order")

    @classmethod
    def find_all(cls) -> List["OrderModel"]:
        return cls.query.all()

    @classmethod
    def find_order_by_id(cls, order_id: int) -> "OrderModel":
        return cls.query.filter_by(id=order_id).first()

    @classmethod
    def find_user_orders(cls, user_id: int) -> List["OrderModel"]:
        return cls.query.filter_by(user_id=user_id).order_by(OrderModel.order_date)

    def save_order(self):
        db.session.add(self)
        db.session.commit()

    def delete_order(self):
        db.session.delete(self)
        db.session.commit()
