from flask import redirect, render_template, request, flash, url_for, abort
from flask_login import current_user, login_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

from . import bp
from belka.models import db, Api, Field, Data


@bp.get('/')
@login_required
def index():
    q = db.select(Api, db.func.count(Data.id))\
        .outerjoin(Data)\
        .filter(Api.user_id == current_user.id)\
        .group_by(Api.id)\
        .order_by(Api.created)

    apis = db.session.execute(q).all()

    return render_template('my/index.html', apis=apis)


class ApiForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    title = StringField('name')
    description = StringField('name')


@bp.route('/create', methods=['GET', 'POST'])
@bp.route('/apis/<int:api_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(api_id=None):
    if api_id:
        q = db.select(Api).filter_by(user_id=current_user.id, id=api_id)
        api = db.one_or_404(q, description='API не найден. Удалили, может?')
    else:
        api = Api(user_id=current_user.id, active=True)

    form = ApiForm(obj=api)

    if form.validate_on_submit():
        ok = True
        if api.id is None:
            q = db.select(Api).filter_by(name=form.name.data)
            existing = db.session.execute(q).scalars().all()
            print(existing)
            if existing:
                flash('Это имя уже занято', 'danger')
                ok = False

        if ok:
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


@bp.get('/apis/<int:api_id>/data')
@login_required
def data(api_id):
    q = db.select(Api).filter_by(user_id=current_user.id, id=api_id)
    api = db.one_or_404(q, description='API не найден. Удалили, может?')

    q = db.select(Data).filter_by(api_id=api.id).order_by(Data.sort)
    data = db.session.execute(q).scalars()

    return render_template('my/data.html', api=api, data=data)


@bp.post('/apis/<int:api_id>/data')
def data_add(api_id):
    q = db.select(Api).filter_by(user_id=current_user.id, id=api_id)
    api = db.one_or_404(q, description='API не найден. Удалили, может?')

    obj = Data(api_id=api.id)
    obj.content = {}

    q = db.select(db.func.max(Data.sort)).filter_by(api_id=api.id)
    s = db.session.execute(q).scalar_one_or_none() or 0
    obj.sort = s + 1

    for field in api.fields:
        obj.content[field.name] = field.coerce(request.form.get(field.name))

    db.session.add(obj)
    db.session.commit()

    return redirect(url_for('.data', api_id=api.id))


@bp.post('/api/<int:api_id>/data/delete')
def data_delete(api_id):
    q = db.select(Api).filter_by(user_id=current_user.id, id=api_id)
    api = db.one_or_404(q, description='API не найден. Удалили, может?')

    db.session.execute(db.delete(Data).filter_by(api_id=api.id, id=request.form['obj_id']))
    db.session.commit()

    return redirect(url_for('.data', api_id=api.id))
