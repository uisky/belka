from flask import Blueprint

bp = Blueprint('my', __name__, url_prefix='/my')

from . import views
