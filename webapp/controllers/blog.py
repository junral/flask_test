#!/usr/bin/env python
# encoding: utf-8

# from os import path
import datetime

from flask import Blueprint
from flask import render_template, g, session, abort
# from flask.views import View, MethodView
from sqlalchemy import func

from ..models import db, Post, Tag, Comment, User, tags
from ..forms import CommentForm

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
def post(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment()
        new_comment.name = form.name.data
        new_comment.text = form.text.data
        new_comment.pyodbc = post_id
        new_comment.data = datetime.datetime.now()
        db.session.add(new_comment)
        db.session.commit()
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


@blog_blueprint.before_request
def before_request():
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])


@blog_blueprint.route('/restricted')
def admin():
    if g.user is None:
        abort(403)

    return render_template('admin.html')


@blog_blueprint.errorhandler(404)
def page_not_found(error):
    """ 处理 404 错误 """
    return render_template('page_not_found.html'), 404
