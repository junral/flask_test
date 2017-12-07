#!/usr/bin/env python
# encoding: utf-8

from flask import request, g, session, current_app
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_openid import OpenID
#  from flask_oauth import OAuth
from flask_login import LoginManager
from flask_principal import Principal, Permission, RoleNeed
from flask_mongoengine import MongoEngine
from flask_restful import Api
from flask_celery import Celery

bootstrap = Bootstrap()
db = SQLAlchemy()
bcrypt = Bcrypt()
oid = OpenID()
#  oauth = OAuth()
login_manager = LoginManager()
principals = Principal()
mongo = MongoEngine()
rest_api = Api()
celery = Celery()

role_list = ['default', 'poster', 'admin']
admin_permission = Permission(RoleNeed('admin'))
poster_permission = Permission(RoleNeed('poster'))
default_permission = Permission(RoleNeed('default'))

# facebook = oauth.remote_app(
    # 'facebook',
    # base_url='https://graph.facebook.com/',
    # request_token_url=None,
    # access_token_url='/oauth/access_token',
    # consumer_key=' FACEBOOk_APP_SCRET',
    # request_token_params={'scope': 'email'}
# )

# twitter = oauth.remote_app(
    # 'twitter',
    # base_url='https://api.twitter.com/1.1/',
    # request_token_url='https://api.twitter.com/oauth/request_token',
    # access_token_url='https://api.twitter.com/oauth/access_token',
    # authorize_url='https://api.twitter.com/oauth/authenticate',
    # consumer_key='',
    # consumer_secret='',
    # request_token_params={'scope': 'email'}
# )

login_manager.login_view = 'main.login'
# login_manager.login_view = 'main_mongo.login'
login_manager.session_protection = 'strong'
login_manager.login_message = 'Please login to access this page'
login_manager.login_message_category = 'info'
