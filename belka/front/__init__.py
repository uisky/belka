from flask import Blueprint

bp = Blueprint('front', __name__, url_prefix='/')

from . import views, users
