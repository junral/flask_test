#!/usr/bin/env python
# encoding: utf-8

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from config import DevConfig

app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)


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


@app.route('/')
@app.route('/<int:page>')
def home(page=1):
    # return '<h1>Hello World!</h1>'
    posts = Post.query.order_by(
        Post.publish_date.desc()
    ).pagination(page, 10)
    recent, top_tags = sidebar_data()

    return render_template(
        'home.html',
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )


if __name__ == '__main__':
    app.run()
