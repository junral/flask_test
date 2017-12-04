#!/usr/bin/env python
# encoding: utf-8

import datetime

from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask import Blueprint
from flask import redirect, url_for
from flask import  render_template, g, session, abort
from flask.views import View, MethodView
from sqlalchemy import func
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Required, Length

from config import DevConfig

app = Flask(__name__)
app.config.from_object(DevConfig)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


# 表单 forms
class CommentForm(FlaskForm):
    """ 评论的表单 """
    name = StringField('Name', validators=[Required(), Length(max=255)])
    text = TextAreaField('Comment', validators=[Required()])
    submit = SubmitField('Add Comment')


def custom_email(form, field):
    """ 自定义表单邮箱验证 """
    import re
    import wtforms
    if not re.match(r'[^@]+@[^@]+\.[^@]+', field.data):
        raise wtforms.ValidationError('Field must be a valid email address.')


# 模型 models
class User(db.Model):
    """ 用户表 """

    # 数据库表明
    __tablename__ = 'user'

    # 主键
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    # 在 SQLAlchem 中创建虚拟的列，和 Post 表中的外键建立联系
    posts = db.relationship('Post', backref='user', lazy='dynamic')

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return r"<User '{}'>".format(self.username)


# 针对 Post 表和 Tag 表的多对多关系管理
tags = db.Table(
    'tags',
    db.Column('post_id', db.Integer(), db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer(), db.ForeignKey('tag.id'))
)


class Post(db.Model):
    """ 博客文章表 """
    __tablename__ = 'post'

    # 主键
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime())
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    # 外键
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    # secondary 参数会告知 SQLAlchemy 该关联别保存在 tags 表里
    tags = db.relationship(
        'Tag',
        secondary=tags,
        backref=db.backref('posts', lazy='dynamic')
    )

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return r"<Post'{}'>".format(self.title)

    @staticmethod
    def generate_fake_posts(num=100):
        import random
        import datetime
        user = User.query.get(1)
        tag_one = Tag('Python')
        tag_two = Tag('Flask')
        tag_three = Tag('SQLAlchemy')
        tag_four = Tag('Jinja')
        tag_list = [tag_one, tag_two, tag_three, tag_four]

        s = "Example text"

        for i in range(num):
            new_post = Post("Post " + str(i))
            new_post.user = user
            new_post.publish_date = datetime.datetime.now()
            new_post.text = s
            new_post.tags = random.sample(tag_list, random.randint(1, 3))
            db.session.commit()


class Comment(db.Model):
    """ 评论表 """
    __tablename__ = 'comment'

    # 主键
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    text = db.Column(db.Text())
    date = db.Column(db.DateTime())
    # 外键
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'))

    def __repr__(self):
        return "<Comment '{}'>".format(self.text[:15])


class Tag(db.Model):
    """ 标签表 """
    __tablename__ = 'tag'

    # 主键
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return "<Tag '{}'>".format(self.title)


def sidebar_data():
    recent = Post.query.order_by(Post.publish_date.desc()).limit(5).all()
    top_tags = db.session.query(
        Tag, func.count(tags.c.post_id).label('total')
    ).join(
        tags
    ).group_by(Tag).order_by('total DESC').limit(5).all()

    return recent, top_tags


blog_blueprint = Blueprint(
    'blog',
    __name__,
    template_folder='templates/blog',
    # static_folder='static/blog',
    url_prefix='/blog'
)


@blog_blueprint.route('/')
@blog_blueprint.route('/<int:page>')
def home(page=1):
    # return '<h1>Hello World!</h1>'
    posts = Post.query.order_by(
        Post.publish_date.desc()
    )  # .pagination(page, 10)
    recent, top_tags = sidebar_data()

    return render_template(
        'home.html',
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )


# @app.route('/post/<int:post_id>')
# def post(post_id):
# post = Post.query.get_or_404(post_id)
# tags = post.tags
# comments = post.comments.order_by(Comment.date.desc()).all()
# recent, top_tags = sidebar_data()

    # return render_template(
    # 'post.html',
    # post=post,
    # tags=tags,
    # comments=comments,
    # recent=recent,
    # top_tags=top_tags
    # )


@blog_blueprint.route('/tag/<string:tag_name>')
def tag(tag_name):
    tag = Tag.query.filter_by(title=tag_name).first_or_404()
    posts = tag.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template(
        'tag.html',
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
        'user.html',
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
        'post.html',
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


@app.route('/')
def index():
    return redirect(url_for('blog.home'))


app.register_blueprint(blog_blueprint)


if __name__ == '__main__':
    app.run()
