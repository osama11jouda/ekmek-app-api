from typing import List

from db import db


class AddressModel(db.Model):
    __tablename__ = "user_address"

    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(128), nullable=False)
    city = db.Column(db.String(128), nullable=False)
    street = db.Column(db.String(128), nullable=False)
    address_detail = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))

    @classmethod
    def find_address_by_user(cls, user_id: int) -> "AddressModel":
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def find_all(cls) -> List['AddressModel']:
        return cls.query.all()

    def save_address(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_address(self) -> None:
        db.session.delete(self)
        db.session.commit()


