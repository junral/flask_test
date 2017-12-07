#!/usr/bin/env python
# encoding: utf-8

from flask import Blueprint
from flask import render_template, redirect, url_for, flash, abort
from flask import request, session, g, current_app

from flask_login import login_user, logout_user, login_required
from flask_principal import Identity, AnonymousIdentity, identity_changed

from ..models import User
from ..forms import LoginForm, RegisterForm, OpenIDForm
from ..extensions import (
    oid,
    #  facebook,
    #  twitter,
    login_manager

)


auth_blueprint = Blueprint(
    'auth',
    __name__,
    #  template_folder='templates/auth'
)


@auth_blueprint.route('/restricted')
def admin():
    if g.user is None:
        abort(403)

    return render_template('admin.html')


@auth_blueprint.errorhandler(404)
def page_not_found(error):
    """ 处理 404 错误 """
    return render_template('404.html'), 404


@auth_blueprint.route('/')
def index():
    return redirect(url_for('blog.home'))


@auth_blueprint.route('/login', methods=['GET', 'POST'])
# 告诉 Flask-OpenID 接受从中继方返回的认证信息。
@oid.loginhandler
def login():
    form = LoginForm()
    openid_form = OpenIDForm()

    if openid_form.validate_on_submit():
        return oid.try_login(
            openid_form.openid.openid.data,
            ask_for=['nickname', 'email'],
            ask_for_optional=['fullname']
        )

    if form.validate_on_submit():
        # Add the user's name to the cookie
        # session['username'] = form.username.data
        user = User.query.filter_by(
            username=form.username.data
        ).one()
        login_user(user, remember=form.remember.data)

        identity_changed.send(
            current_app._get_current_object(),
            identity=Identity(user.id)
        )

        flash('You have been logged in.', category='success')
        return redirect(url_for('blog.home'))

    openid_errors = oid.fetch_error()
    if openid_errors:
        flash(openid_errors, category='danger')

    return render_template('auth/login.html', form=form)


@auth_blueprint.route('/register', methods=['GET', 'POST'])
@oid.loginhandler
def regester():
    form = RegisterForm()
    openid_form = OpenIDForm()

    if openid_form.validate_on_submit():
        return oid.try_login(
            openid_form.openid.openid.data,
            ask_for=['nickname', 'email'],
            ask_for_optional=['fullname']
        )

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        User.create(username, email, password)

        flash(
            'Your user has been created, please login.',
            category='success'
        )

        return redirect(url_for('.login'))

    openid_errors = oid.fetch_error()
    if openid_errors:
        flash(openid_errors, category='danger')

    return render_template('auth/register.html', form=form)


@auth_blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    # Remove the username from the cookie
    # session.pop('usename', None)
    logout_user()
    identity_changed.send(
        current_app._get_current_object(),
        identity=AnonymousIdentity()
    )

    flash('You have been logged out.', category='success')

    return redirect(url_for('.login'))


@login_manager.user_loader
def load_user(userid):
    from ..models import User
    return User.query.get(userid)


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


#  # facebook 登录
#  @auth_blueprint.route('/facebook')
#  def facebook_login():
    #  return facebook.authorize(
        #  callback=url_for(
            #  '.facebook_authorized',
            #  next=request.referrer or None,
            #  _external=True
        #  )
    #  )


#  @auth_blueprint.route('/facebook/authorized')
#  @facebook.authorized_hander
#  def facebook_authorized(resp):
    #  if resp is None:
        #  return 'Access denied: reason=%s error=%s' % (
            #  request.args['error_reason'],
            #  request.args['error_description']
        #  )

    #  session['facebook_oauth_token'] = (resp['access_token'], '')

    #  me = facebook.get('/me')
    #  user = User.query.filter_by(
    #  ).first()

    #  if not user:
        #  User.create(me.data['first_name'] + ' ' + me.data['last_name'])

    #  username=me.data['first_name'] + ' ' + me.data['last_name']
    #  User.create(usename=username)
    #  # 从这里登录用户
    #  flash('You have been logged in.', category="success")

    #  return redirect(request.args.get('next') or url_for('blog.home'))


#  @auth_blueprint.round('/twitter-login')
#  def twitter_login():
    #  return twitter.authorize(
        #  callback=url_for(
            #  '.twitter_authorized',
            #  next=request.referrer or None,
            #  _external=True
        #  )
    #  )


#  @auth_blueprint.route('/twitter-login/authorized')
#  @twitter.authorized_handler
#  def twitter_authenorize(resp):
    #  if resp is None:
        #  return 'Access denied: reason: {} error: {}'.format(
            #  request.args['error_reason'],
            #  request.args['error_description']
        #  )

    #  session['twitter_oauth_token'] = resp['oauth_token'] + \
        #  resp['oauth_token_secret']

    #  user = User.query.filter_by(
        #  username=resp['screen_name']
    #  ).first()

    #  if not user:
        #  User.create(username=resp['screen_name'])

    #  # 从这里登录用户
    #  flash('You have been logged in.', category='success')

    #  return redirect(
        #  request.args.get('next') or url_for('blog.home')
    #  )


# @facebook.tokengetter
# def get_facebook_oauth_token():
    # return session.get('facebook_oauth_token')


# @twitter.tokengetter
# def get_twitter_oauth_token():
    # return session.get('face_oauth_token')
