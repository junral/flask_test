#!/usr/bin/env python
# coding: utf-8

from webapp import create_app
from webapp.models import User, Role
from webapp.extensions import db

app = create_app('test')

db.app = app
db.create_all()

default = Role.create_role('defalut')
poster = Role.create_role('poster')

test_user = User.create(username='test', password='test', roles=poster)

app.run()
