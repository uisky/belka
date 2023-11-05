import uuid
import datetime
import random

from . import db


FIELD_TYPES = {
    'bool': 'Boolean',
    'number': 'Number',
    'string': 'String'
}

FIELD_CONTENT_TYPES = {
    'uuid': 'UUID',
    'date': 'Дата',
    'time': 'Время',
    'datetime': 'Дата и время'
}


class Api(db.Model):
    __tablename__ = 'apis'

    id = db.Column(db.Integer(), primary_key=True)
    created = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.now())
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False, index=True)
    active = db.Column(db.Boolean(), nullable=False, default=True, server_default='t')
    name = db.Column(db.String(64), nullable=False, index=True, unique=True)
    title = db.Column(db.String(256))
    description = db.Column(db.String(4096))

    fields = db.relationship('Field')
    data = db.relationship('Data', back_populates='api')


class Field(db.Model):
    __tablename__ = 'fields'

    id = db.Column(db.Integer(), primary_key=True)
    created = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.now())
    api_id = db.Column(db.Integer(), db.ForeignKey('apis.id'), nullable=False, index=True)

    sort = db.Column(db.SmallInteger(), nullable=False, default=0, server_default='0')
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Enum(*list(FIELD_TYPES.keys()), name='field_type'), nullable=False)

    description = db.Column(db.String(4096))
    content_type = db.Column(db.String(32))

    api = db.relationship('Api', back_populates='fields')

    def default_value(self):
        if self.type == 'number':
            return random.randint(0, 1000)

        elif self.type == 'string':
            if self.content_type == 'uuid':
                return str(uuid.uuid4())
            elif self.content_type == 'date':
                return datetime.date.today().isoformat()
            elif self.content_type == 'time':
                return datetime.datetime.now(datetime.UTC).time().isoformat()
            elif self.content_type == 'datetime':
                return datetime.datetime.now(datetime.UTC).isoformat()
            else:
                return ''

        elif self.type == 'bool':
            return False

    def coerce(self, val):
        if self.type == 'number':
            val = float(val)
            if val == int(val):
                val = int(val)
        elif self.type == 'bool':
            val = bool(val)
        return val
