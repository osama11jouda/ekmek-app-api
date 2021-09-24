from typing import List

from db import db


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    desc = db.Column(db.String(500), nullable=False)
    
    @classmethod
    def find_item_by_id(cls, _id: int) -> "ItemModel":
        return cls.query.filter_by(id=_id).first()
    
    @classmethod
    def find_item_by_name(cls, name: str) -> "ItemModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List['ItemModel']:
        return cls.query.all()
    
    def save_item(self):
        db.session.add(self)
        db.session.commit()
        
    def delete_item(self):
        db.session.delete(self)
        db.session.commit()
