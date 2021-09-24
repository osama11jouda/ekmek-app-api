from db import db


class CodeModel(db.Model):
    __tablename__ = "codes"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer, nullable=False)

