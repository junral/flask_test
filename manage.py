#!/usr/bin/env python
# encoding: utf-8

import os

from flask_script import Manager, Server
from flask_script.commands import ShowUrls, Clean
from flask_migrate import Migrate, MigrateCommand

from webapp import create_app
from webapp.models import db, User, Post, Tag, Comment, Role
# from webapp.models_mongo import db, User, Post, Tag, Comment

env = os.environ.get('WEBAPP', 'default')
app = create_app(env)
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('server', Server())
manager.add_command('show-urls', ShowUrls)
manager.add_command('clean', Clean)
manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post, Comment=Comment, Tag=Tag, Role=Role)


@manager.command
def hello():
    print ("Hello, World!")


@manager.command
def setup_db():
    db.create_all()

    # role_list = (('admin', 'admin'), ('default', 'default'))
    # Role.create_roles(role_list)
    # tag_list = [Tag.create(tag) for tag in ('Python', 'Flask', 'SQLAlchemy', 'Jinja')]
    # default_role = Role.create_role('default', 'default')
    # s = 'Body text'
    admin_role = Role.create_role('admin', 'admin')

    User.create(
        username='admin',
        email='admin@exmaple.com',
        password='password',
        roles=admin_role
    )

    Post.generate_fake_posts()


if __name__ == '__main__':
    manager.run()
