from db import db


class BlockListModel(db.Model):
    __tablename__ = "block_list"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)

    def __init__(self, jti):
        self.jti = jti

    @classmethod
    def find_jti(cls, jti):
        return cls.query.filter_by(jti=jti).scalar()

    def save_jti(self):
        db.session.add(self)
        db.session.commit()
