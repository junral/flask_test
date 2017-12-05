#!/usr/bin/env python
# encoding: utf-8

import os

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from webapp import create_app
from webapp.models import db, User, Post, Tag, Comment
# from webapp.models_mongo import db, User, Post, Tag, Comment

env = os.environ.get('WEBAPP', 'default')
app = create_app(env)
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('server', Server())
manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post, Comment=Comment, Tag=Tag)


if __name__ == '__main__':
    manager.run()
