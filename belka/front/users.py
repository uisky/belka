from flask import redirect, render_template, request, flash, url_for, g
from flask_login import current_user, login_user, logout_user, login_required

from . import bp
from belka.models import db, User


@bp.get('/register/')
def register():
    return render_template('front/register.html')


@bp.post('/register/')
def register_post():
    email = request.form['email'].strip().lower()
    if email == '':
        flash('Email is incorrect', 'danger')
        return redirect('front.register')

    password = request.form['password']
    if len(password) < 6:
        flash('Password should be longer than 6 characters', 'danger')
        return redirect('front.register')

    name = request.form['name'].strip()

    user = User(email=email, password_hash=User.hash_password(password), name=name)
    db.session.add(user)
    db.session.commit()
    login_user(user)

    return redirect(url_for('.index'))


@bp.get('/login/')
def login():
    return render_template('front/login.html')


@bp.post('/login/')
def login_post():
    q = db.select(User) \
        .filter(db.func.lower(User.email) == request.form.get('email').lower(), User.password_hash == User.hash_password(request.form.get('password')))
    user = db.session.execute(q).scalar_one_or_none()

    if not user:
        flash('Invalid email or password.', 'danger')
        return redirect(url_for('.login'))

    login_user(user)
    return redirect(url_for('.index'))


@bp.get('/logout/')
def logout():
    logout_user()
    return redirect(url_for('.index'))


@bp.get('/auth_as/<int:user_id>')
def auth_as(user_id: int):
    user = db.get_or_404(User, user_id)
    login_user(user)
    return redirect(url_for('.index'))
