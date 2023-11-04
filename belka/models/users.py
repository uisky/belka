import hashlib
from flask import current_app, url_for
from flask_login import UserMixin, AnonymousUserMixin
from sqlalchemy.dialects.postgresql import JSONB, ARRAY

from . import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    created = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.now())
    active = db.Column(db.Boolean(), nullable=False, default=True, server_default='t')
    email = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(255), nullable=False)

    @property
    def is_active(self):
        return self.active

    @staticmethod
    def hash_password(data):
        return hashlib.sha256((data + current_app.config['SECRET_KEY']).encode()).hexdigest()


class AnonymousUser(AnonymousUserMixin):
    pass


