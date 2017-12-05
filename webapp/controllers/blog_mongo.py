#!/usr/bin/env python
# encoding: utf-8

from flask import Blueprint
from flask import render_template, redirect, url_for, flash, abort
from flask import g, session
from sqlalchemy import func
from flask_login import login_required, current_user
from flask_principal import Permission, UserNeed

from ..models_mongo import Post, Tag, Comment, User
from ..models_mongo import BlogPost, ImagePost, VideoPost, QuotePost
from ..forms_mongo import CommentForm, PostForm
from ..extensions import poster_permission, admin_permission

blog_mongo_blueprint = Blueprint(
    'blog_mongo',
    __name__,
    template_folder='templates/blog',
    url_prefix='/mongo_blog'
)


def sidebar_data():
    recent = Post.objects.order_by("-publish_date").limit(5).all()
    # top_tags = db.session.query(
        # Tag, func.count(tags.c.post_id).label('total')
    # ).join(
        # tags
    # ).group_by(Tag).order_by('total DESC').limit(5).all()
    tags = [tag for tag in post.tags for post in Post.objects.all()]
    tags = {(tag, tags.count(tag)) for tag in tags}
    sorted_tags = sorted(tags, key=lambda x: x[1])
    top_tags = [tag[0] for tag in sorted_tags[:5]]

    return recent, top_tags
    #  return recent


@blog_mongo_blueprint.route('/')
@blog_mongo_blueprint.route('/<int:page>')
def home(page=1):
    posts = Post.objects.order_by(
        Post.publish_date.desc()
    )
    recent, top_tags = sidebar_data()

    return render_template(
        'blog/home_mongo.html',
        mongo=True,
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )


@blog_mongo_blueprint.route('/tag/<string:tag_name>')
def tag(tag_name):
    tag = Tag.objects(title=tag_name).get_or_404()
    posts = tag.posts.order_by("-publish_date").all()
    recent, top_tags = sidebar_data()

    return render_template(
        'blog/tag.html',
        mongo=True,
        tag=tag,
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )


@blog_mongo_blueprint.route('/user/<string:username>')
def user(username):
    user = User.objects(username=username).get_or_404()
    posts = user.posts.order_by("-publish_date").all()
    recent, top_tags = sidebar_data()

    return render_template(
        'blog/user.html',
        mongo=True,
        user=user,
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )


@blog_mongo_blueprint.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post(post_id):
    post = Post.objects(id=post_id).get_or_404(post_id)
    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment()
        comment.name = form.name.data
        comment.text =  form.text.data
        comment.save()
        post.comments.append(comment)
        post.save()
    tags = post.tags
    comments = post.comments.order_by(Comment.date.desc()).all()

    return render_template(
        'blog/post_mongo.html',
        mongo=True,
        post=post,
        tags=tags,
        comments=comments,
        form=form
    )


@blog_mongo_blueprint.route('/new', methods=['GET', 'POST'])
@login_required
@poster_permission.require(http_exception=403)
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        if form.type.data == 'blog':
            new_post = BlogPost()
            new_post.text = form.text.data
        elif form.type.data == 'image':
            new_post = ImagePost()
            new_post.image_url = form.image.data
        elif form.type.data == 'video':
            new_post = VideoPost()
            new_post.video_object = form.video.data
        elif form.type.data == 'quote':
            new_post = QuotePost()
            new_post.text = form.text.data
            new_post.author = form.tauthor.data
        new_post.title = form.title.data
        new_post.user = current_user
        new_post.save()

    return render_template(
        'blog/new_mongo.html',
        mongo=True,
        form=form)


@blog_mongo_blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
# 创建只希望作者能访问的页面
@poster_permission.require(http_exception=403)
def edit_post(id):
    post = Post.objects(id=id).get_or_404()
    permission = Permission(UserNeed(post.user.id))

    # 同时希望管理员可以修改任何文章
    if permission.can() or admin_permission.can():
        form = PostForm()

        if form.validate_on_submit():
            post.update(
                title=form.title.data,
                text=form.text.data
            )
            post.save()

            return redirect(url_for(
                '.post_mongo.html',
                mongo=True,
                post_id=post.id))

        form.text.data = post.text
        return render_template('blog/edit_mongo.html', form=form, post=post)

    abort(403)


@blog_mongo_blueprint.before_request
def before_request():
    """ 在所有请求处理之前运行 """
    if 'username' in session:
        g.user = User.query.get(session['usename']).one()
    else:
        g.crrent_user = None
