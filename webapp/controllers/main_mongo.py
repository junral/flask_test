#!/usr/bin/env python
# encoding: utf-8

from flask import Blueprint
from flask import render_template, redirect, url_for, flash, abort
from flask import request, session, g, current_app

from flask_login import login_user, logout_user, login_required
from flask_principal import Identity, AnonymousIdentity, identity_changed

from ..models_mongo import User
from ..forms_mongo import LoginForm, RegisterForm, OpenIDForm
from ..extensions import oid
# from ..extensions import facebook, twitter


main_mongo_blueprint = Blueprint(
    'main_mongo',
    __name__,
    url_prefix='/mongo'
)


@main_mongo_blueprint.route('/restricted')
def admin():
    if g.user is None:
        abort(403)

    return render_template(
        'admin.html',
        mongo=True
    )


@main_mongo_blueprint.errorhandler(404)
def page_not_found(error):
    """ 处理 404 错误 """
    return render_template('page_not_found.html'), 404


@main_mongo_blueprint.route('/')
def index():
    return redirect(url_for(
        'blog_mongo.home',
        mongo=True
    ))


@main_mongo_blueprint.route('/login', methods=['GET', 'POST'])
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
        user = User.objects(username=form.username.data).one()
        login_user(user, remember=form.remember.data)

        identity_changed.send(
            current_app._get_current_object(),
            identity=Identity(user.id)
        )

        flash('You have been logged in.', category='success')

    openid_errors = oid.fetch_error()
    if openid_errors:
        flash(openid_errors, category='danger')

    return render_template(
        'login_mongo.html',
        mongo=True,
        form=form
    )


@main_mongo_blueprint.route('/register', methods=['GET', 'POST'])
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
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.set_password(form.password.data)
        user.save()

        flash(
            'Your user has been created, please login.',
            category='success'
        )

        return redirect(url_for(
            '.login',
            mongo=True))

    openid_errors = oid.fetch_error()
    if openid_errors:
        flash(openid_errors, category='danger')

    return render_template(
        'register_mongo.html',
        mongo=True,
        form=form
    )


@main_mongo_blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    identity_changed.send(
        current_app._get_current_object(),
        identity=AnonymousIdentity()
    )

    flash('You have been logged out.', category='success')

    return redirect(url_for(
        '.login',
        mongo=True
    ))


#  # facebook 登录
#  @main_mongo_blueprint.route('/facebook')
#  def facebook_login():
    #  return facebook.authorize(
        #  callback=url_for(
            #  '.facebook_authorized',
            #  next=request.referrer or None,
            #  _external=True
        #  )
    #  )


#  @main_mongo_blueprint.route('/facebook/authorized')
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
        #  username=me.data['first_name'] + ' ' + me.data['last_name']
    #  ).first()

    #  if not user:
        #  User.create_user(me.data['first_name'] + ' ' + me.data['last_name'])

    #  # 从这里登录用户
    #  flash('You have been logged in.', category="success")

    #  return redirect(request.args.get('next') or url_for('blog.home'))


#  @main_mongo_blueprint.round('/twitter-login')
#  def twitter_login():
    #  return twitter.authorize(
        #  callback=url_for(
            #  '.twitter_authorized',
            #  next=request.referrer or None,
            #  _external=True
        #  )
    #  )


#  @main_mongo_blueprint.route('/twitter-login/authorized')
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
        #  User.create_user(username=resp['screen_name'])

    #  # 从这里登录用户
    #  flash('You have been logged in.', category='success')

    #  return redirect(
        #  request.args.get('next') or url_for('blog.home')
    #  )
