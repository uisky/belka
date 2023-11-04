import os

from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_migrate import Migrate

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

    # ORM & migrations
    db.init_app(app)
    Migrate(app, db)

    # Blueprints
    from belka import front, my
    app.register_blueprint(front.bp)
    app.register_blueprint(my.bp)

    # Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.anonymous_user = AnonymousUser

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # Jinja
    init_jinja(app)

    # CLI
    init_commands(app)

    return app

