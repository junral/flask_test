#!/usr/bin/env python
# encoding: utf-8

from flask import redirect, url_for, flash
from flask import request, g, session, current_app
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_openid import OpenID
# from flask_oauth import OAuth
from flask_login import LoginManager
from flask_principal import Principal, Permission, RoleNeed
from flask_mongoengine import MongoEngine

bootstrap = Bootstrap()
db = SQLAlchemy()
bcrypt = Bcrypt()
oid = OpenID()
# oauth = OAuth()
login_manager = LoginManager()
principals = Principal()
mongo = MongoEngine()

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


@oid.after_login
def create_or_login(resp):
    from .models import User

    username = resp.fullname or resp.nickname
    email = resp.email
    if not username and not email:
        flash('Invalid login. Please try again.', 'danger')
        return redirect(url_for('main.login'))

    user = User.query.filter_by(username=username, email=email).first()
    if user is None:
        User.create_user(username, email)

    # 在这里登录用户
    return redirect(url_for('blog.home'))


# @facebook.tokengetter
# def get_facebook_oauth_token():
    # return session.get('facebook_oauth_token')


# @twitter.tokengetter
# def get_twitter_oauth_token():
    # return session.get('face_oauth_token')


@login_manager.user_loader
def load_user(userid):
    from Model import User
    return User.query.get(userid)
