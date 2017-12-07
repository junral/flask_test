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
from flask_debugtoolbar import DebugToolbarExtension
from flask_cache import Cache
from flask_assets import Environment, Bundle
from flask_admin import Admin
from flask_mail import Mail
from flask_babel import Babel

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
debug_toolbar = DebugToolbarExtension()
cache = Cache()
assets_env = Environment()
main_css = Bundle(
    'css/bootstrap.css',
    filters='cssmin',
    output='css/common.css'
)

main_js = Bundle(
    'js/query.js',
    'js/bootstrap.js',
    filters='jsmin',
    output='js/common.js'
)
admin = Admin()
mail = Mail()
babel = Babel()

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
