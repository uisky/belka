import os

from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from belka.models import db, User, AnonymousUser
from belka.jinja import init_jinja
from belka.commands import init_commands


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    os.makedirs(app.instance_path, exist_ok=True)

    # Configs
    app.config.from_pyfile(os.path.join(app.root_path, 'config.py'))
    if test_config is None:
        # Try to load host-specific config from instance/config.py
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    app.json.ensure_ascii = False
    app.json.sort_keys = True
    app.json.compact = False

    # ORM & migrations
    db.init_app(app)
    Migrate(app, db)

    # Blueprints
    from belka import front, my, api
    app.register_blueprint(front.bp)
    app.register_blueprint(my.bp)
    app.register_blueprint(api.bp)

    # Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.anonymous_user = AnonymousUser
    login_manager.login_view = 'front.login'
    login_manager.login_message = 'Чтобы этим пользоваться, нужно войти или зарегаться'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # Jinja
    init_jinja(app)

    # CLI
    init_commands(app)

    # CSRF
    CSRFProtect(app)

    return app

