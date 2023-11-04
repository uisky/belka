from sqlalchemy.dialects.postgresql import ARRAY

from . import db


MEASURES = {
    'service': {'title': 'За услугу'},
    'minute': {'title': 'За минуту'},
    'hour': {'title': 'За час'},
    'day': {'title': 'За день'},
    'week': {'title': 'За неделю'},
    'month': {'title': 'За месяц'},
    'meter': {'title': 'За метр'},
    'linear_meter': {'title': 'За погонный метр'},
    'square_meter': {'title': 'За квадратный метр'},
    'kilometer': {'title': 'За километр'},
    'kilogram': {'title': 'За килограмм'},
    'tonn': {'title': 'За тонну'},
    'lesson': {'title': 'За урок'},
    'piece': {'title': 'За час'},
    '1000let': {'title': 'За 1000 символов'},
}


class ServiceCat(db.Model):
    __tablename__ = 'service_cats'

    id = db.Column(db.Integer(), primary_key=True)
    # Materialized path
    mp = db.Column(ARRAY(db.Integer(), zero_indexes=True), nullable=False, index=True)
    parent_id = db.Column(db.Integer(), db.ForeignKey('service_cats.id'), index=True)
    name = db.Column(db.String(255), nullable=False)
    remote_ok = db.Column(db.Boolean(), nullable=False, default=False, server_default='f')
    # MEASURES.keys()
    available_measures = db.Column(ARRAY(db.String(16), zero_indexes=True))
