from flask import redirect, render_template, request, flash, url_for, abort
from flask_login import current_user, login_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

from . import bp
from belka.models import db, Api, Field


@bp.get('/')
@login_required
def index():
    q = db.select(Api)\
        .filter_by(user_id=current_user.id)\
        .order_by(Api.created)
    apis = db.session.execute(q).scalars().all()

    return render_template('my/index.html', apis=apis)


class ApiForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    title = StringField('name')
    description = StringField('name')
    active = BooleanField('active')


@bp.route('/create', methods=['GET', 'POST'])
@bp.route('/apis/<int:api_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(api_id=None):
    if api_id:
        q = db.select(Api).filter_by(user_id=current_user.id, id=api_id)
        api = db.one_or_404(q, description='API не найден. Удалили, может?')
    else:
        api = Api(user_id=current_user.id)

    form = ApiForm(obj=api)

    if form.validate_on_submit():
        form.populate_obj(api)
        db.session.add(api)
        db.session.flush()

        if api.id:
            db.session.execute(db.delete(Field).filter_by(api_id=api.id))
        for i, f_sort in enumerate(request.form.getlist('f_sort')):
            field = Field(api_id=api.id, sort=f_sort)
            field.name = request.form.getlist('f_name')[i]
            field.type = request.form.getlist('f_type')[i]
            field.content_type = request.form.getlist('f_content_type')[i]
            db.session.add(field)

        db.session.commit()

        return redirect(url_for('.index'))

    return render_template('my/edit.html', api=api, form=form)

