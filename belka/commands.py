import click
import random
import string
from belka.models import db, User


def gen_password(length=12):
    return ''.join([random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(length)])


def init_commands(app):
    @app.cli.command('user-create')
    @click.argument("email")
    @click.argument("name")
    def user_create(email, name):
        if User.query.filter(db.func.lower(User.email) == email.lower()).first() is not None:
            click.echo(f'User with email "{email}" already exists.')
            return

        user = User(email=email, name=name)
        password = input('Password (Enter * to generate): ')
        if password == '*':
            password = gen_password()
            click.echo(f'Password is {password}')

        user.password_hash = User.hash_password(password)
        db.session.add(user)
        db.session.commit()
        click.echo(f'Admin {email} "{name}" created')
