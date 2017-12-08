#!/usr/bin/env python
# encoding: utf-8

# import datetime
# from urllib.parse import urlencode

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    abort,
    g,
    session,
    request,
    current_app
)
# from flask.views import View, MethodView
from sqlalchemy import func
from flask_login import login_required, current_user
from flask_principal import Permission, UserNeed

from ..models import Post, Tag, Comment, User, tags
from ..forms import CommentForm, PostForm
from ..extensions import (
    db,
    poster_permission,
    admin_permission,
    cache,
    babel,
    youtube
)

blog_blueprint = Blueprint(
    'blog',
    __name__,
    template_folder='templates/blog',
    # static_folder='static/blog',
    url_prefix='/blog'
)


# key_prefix 用于指定再次调用的函数
@cache.cached(timeout=7200, key_prefix='sidebar_data')
def sidebar_data():
    recent = Post.query.order_by(
        Post.publish_date.desc()).limit(5).all()

    top_tags = db.session.query(
        Tag, func.count(tags.c.post_id).label('total')
    ).join(
        tags
    ).group_by(
        Tag
    ).order_by('total DESC').limit(5).all()

    return recent, top_tags


@blog_blueprint.route('/')
@blog_blueprint.route('/<int:page>')
# timeout 参数表示结果将会缓存多少秒，超过这个时长之后，就会再次执行该函数并缓存
# 结果
@cache.cached(timeout=60)
def home(page=1):
    # return '<h1>Hello World!</h1>'
    posts_query = Post.query.order_by(
        Post.publish_date.desc()
    )
    posts = posts_query.all()
    pagination = posts_query.paginate(
        page,
        per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False
    )
    recent, top_tags = sidebar_data()

    return render_template(
        'blog/home.html',
        posts=posts,
        pagination=pagination,
        recent=recent,
        top_tags=top_tags
    )


@blog_blueprint.route('/tag/<string:tag_name>')
def tag(tag_name):
    tag = Tag.query.filter_by(
        title=tag_name).first_or_404()

    posts = tag.posts.order_by(
        Post.publish_date.desc()).all()

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
    user = User.query.filter_by(
        username=username).first_or_404()

    posts = user.posts.order_by(
        Post.publish_date.desc()).all()

    recent, top_tags = sidebar_data()

    return render_template(
        'blog/user.html',
        user=user,
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )


@babel.localeselector
def get_locale():
    # if a user is logged in, use the local from the user settings
    user = getattr(g, 'user', None)
    if user is not None:
        return user.locale
    # otherwise try to guess the language from the user accept
    # header the browser tranmits. We support de/fr/en in this
    # example. The best match wins.
    return request.accept_languages.best_match(['de', 'fr', 'en'])


@babel.timezoneselector
def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone


def make_cache_key(*args, **kwargs):
    path = request.path
    args = str(hash(frozenset(request.args.items())))
    lang = get_locale()
    return (path + args + lang).encode('utf-8')


@blog_blueprint.route('/post/<int:post_id>', methods=['GET', 'POST'])
@cache.cached(timeout=600, key_prefix=make_cache_key)
@login_required
def post(post_id):
    form = CommentForm()
    post = Post.query.get_or_404(post_id)

    if form.validate_on_submit():
        name = form.name.data
        text = form.text.data
        Comment.create(name, text, post.id, current_user.id)

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
        new_post = Post.create(title, text, current_user.id)
        if new_post is None:
            flash(
                'The new post create unsuccess',
                category='danger'
            )

    return render_template(
        'blog/new.html',
        form=form
    )


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
