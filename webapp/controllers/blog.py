#!/usr/bin/env python
# encoding: utf-8

# from os import path
# import datetime

from flask import Blueprint
from flask import render_template, redirect, url_for, flash, abort
from flask import g, session
# from flask.views import View, MethodView
from sqlalchemy import func
from flask_login import login_required
from flask_principal import Permission, UserNeed

from ..models import Post, Tag, Comment, User, tags
from ..forms import CommentForm, PostForm
from ..extensions import db, poster_permission, admin_permission

blog_blueprint = Blueprint(
    'blog',
    __name__,
    template_folder='templates/blog',
    # static_folder='static/blog',
    url_prefix='/blog'
)


def sidebar_data():
    recent = Post.query.order_by(Post.publish_date.desc()).limit(5).all()
    top_tags = db.session.query(
        Tag, func.count(tags.c.post_id).label('total')
    ).join(
        tags
    ).group_by(Tag).order_by('total DESC').limit(5).all()

    return recent, top_tags


@blog_blueprint.route('/')
@blog_blueprint.route('/<int:page>')
def home(page=1):
    # return '<h1>Hello World!</h1>'
    posts = Post.query.order_by(
        Post.publish_date.desc()
    )  # .pagination(page, 10)
    recent, top_tags = sidebar_data()

    return render_template(
        'blog/home.html',
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )


@blog_blueprint.route('/tag/<string:tag_name>')
def tag(tag_name):
    tag = Tag.query.filter_by(title=tag_name).first_or_404()
    posts = tag.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template(
        'blog/tag.html',
        tag=tag,
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )


@blog_blueprint.route('/user/<string:username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template(
        'blog/user.html',
        user=user,
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )


@blog_blueprint.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post(post_id):
    form = CommentForm()

    if form.validate_on_submit():
        name = form.name.data
        text =  form.text.data
        Comment.create_comment(name, text, post_id)

    post = Post.query.get_or_404(post_id)
    tags = post.tags
    comments = post.comments.order_by(Comment.date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template(
        'blog/post.html',
        post=post,
        tags=tags,
        comments=comments,
        recent=recent,
        top_tags=top_tags,
        form=form
    )


@blog_blueprint.route('/new', methods=['GET', 'POST'])
@login_required
@poster_permission.require(http_exception=403)
def new_post():
    if not g.current_user:
        return redirect(url_for('main.login'))

    form = PostForm()

    if form.validate_on_submit():
        title = form.title.data
        text = form.text.data
        Post.create_post(title, text)

    return render_template('blog/new.html', form=form)


@blog_blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
# 创建只希望作者能访问的页面
@poster_permission.require(http_exception=403)
def edit_post(id):
    #  if not g.current_user:
        #  return redirect(url_for('main.login'))

    post = Post.query.get_or_404(id)
    permission = Permission(UserNeed(post.user.id))

    # 同时希望管理员可以修改任何文章
    if permission.can() or admin_permission.can():
        form = PostForm()

        if form.validate_on_submit():
            title = form.title.data
            text = form.text.data
            post.change(title, text)

            return redirect(url_for('.post', post_id=post.id))

        form.text.data = post.text
        return render_template('blog/edit.html', form=form, post=post)

    abort(403)


@blog_blueprint.before_request
def before_request():
    """ 在所有请求处理之前运行 """
    #  if 'user_id' in session:
        #  g.user = User.query.get(session['user_id'])

    if 'username' in session:
        g.user = User.query.get(session['usename']).one()
    else:
        g.crrent_user = None
