from sqlalchemy.dialects.postgresql import JSONB

from . import db


class Data(db.Model):
    __tablename__ = 'data'

    id = db.Column(db.Integer(), primary_key=True)
    created = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.now())
    api_id = db.Column(db.Integer(), db.ForeignKey('apis.id'), nullable=False, index=True)

    sort = db.Column(db.SmallInteger(), nullable=False, default=0, server_default='0')
    content = db.Column(JSONB(), nullable=False)

    api = db.relationship('Api')


