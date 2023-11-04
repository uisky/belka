from sqlalchemy.dialects import postgresql
from flask import redirect, render_template, request, flash, url_for, abort
from flask_login import current_user, login_user, logout_user, login_required

from . import bp
from belka.models import db, User


@bp.get('/')
def index():
    return render_template('front/index.html')


