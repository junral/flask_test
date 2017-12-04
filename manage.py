#!/usr/bin/env python
# encoding: utf-8

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from main import app, db, User, Post, Comment, Tag, tags

migrate = Migrate(app, db)

manager = Manager(app)

manager.add_command('server', Server())
manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post, Comment=Comment, Tag=Tag, tags=tags)


if __name__ == '__main__':
    manager.run()