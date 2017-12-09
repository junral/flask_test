#!/usr/bin/env python
# encoding: utf-8

from gzip import GzipFile
from io import BytesIO

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


class Gzip(object):

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.after_request(self.after_request)

    def after_request(self, response):
        encoding = request.headers.get('Accept-Encoding', '')

        if 'gzip' not in encoding or not response.status_code in (200, 201):
            return response

        response.direct_passthrough = False

        contents = BytesIO()
        with GzipFile(
            mode='wb',
            compresslevel=5,
            fileobj=contents) as gzip_file:
            gzip_file.write(response.get_date())

        response.set_data(bytes(contents.getvalue()))

        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Content-Length'] = response.content_length

        return response

flask_gzip = Gzip()
