from typing import List

from db import db
from models.address_model import AddressModel


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_image = db.Column(db.String(255), nullable=True)
    registered_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_delivery = db.Column(db.Boolean, nullable=False, default=False)
    current_balance = db.Column(db.Integer, nullable=True, default=0)

    address = db.relationship("AddressModel", lazy="dynamic")

    "applied codes model - one tp many"
    "orders model one to many"
    "confirmations model one to many"

    @classmethod
    def find_user_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_user_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_all(cls) -> List['UserModel']:
        return cls.query.all()

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()
