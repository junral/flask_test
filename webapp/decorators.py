#!/usr/bin/env python
# encoding: utf-8

from flask import redirect, url_for, flash

from .extensions import oid, login_manager
# from .extensions import facebook, twitter


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
    from .models import User
    return User.query.get(userid)
