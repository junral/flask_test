#!/usr/bin/env python
# encoding: utf-8

import datetime

from flask_login import AnonymousUserMxin

from .extensions import db, bcrypt


# 模型 models
roles = db.Table(
    'role_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
)


class User(db.Model):
    """ 用户表 """

    # 数据库表明
    __tablename__ = 'user'

    # 主键
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    # 在 SQLAlchem 中创建虚拟的列，和 Post 表中的外键建立联系
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    roles = db.relationship('Role', secondary=roles, lazy='dynamic')

    def __init__(self, username):
        self.username = username
        default = Role.query.filter_by(name='defalut').one()
        self.roles.append(default)

    def __repr__(self):
        return r"<User '{}'>".format(self.username)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def is_authenicated(self):
        if isinstance(self, AnonymousUserMxin):
            return False
        else:
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        if isinstance(self, AnonymousUserMxin):
            return True
        else:
            return False

    def get_id(self):
        return str(self.id)

    @staticmethod
    def create_user(username='', email='', password=None):
        if username or email:
            new_user = User()
            new_user.username = username
            new_user.email = email
            if password:
                new_user.set_password(password)

            db.session.add(new_user)
            db.session.commit()


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Role {}>'.format(self.name)


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

    def change(self, title, text=''):
        """
        Chang the post data.

        Args:
            title(str): the title of the psot.
            Text(str): the content of the psot.
        """
        self.title = title
        self.text = text
        self.publish_date = datetime.datetime.now()

        db.session.add(self)
        db.session.commit

    @staticmethod
    def create_post(title, text='', user_id=0, *tags):
        """
        Create a new post to database.

        Args:
            title(str): the title of the psot.
            Text(str): the content of the psot.
            user_id(int): the ID of user who the post belongs to.
            *tag: a set of tag.
        """

        new_post = Post(title)
        new_post.text = text
        new_post.publish_date = datetime.datetime.now()
        new_post.user_id = user_id
        for tag in tags:
            new_post.tags.appen(tag)
        db.session.add(new_post)
        db.session.commit()

    @staticmethod
    def generate_fake_posts(num=100):
        """
        Generate some test datas with tags.

        Args:
            num: the numbers of the data want to generate.
        """
        import random
        user = User.query.get(1)
        tag_one = Tag('Python')
        tag_two = Tag('Flask')
        tag_three = Tag('SQLAlchemy')
        tag_four = Tag('Jinja')
        tag_list = [tag_one, tag_two, tag_three, tag_four]

        s = "Example text"

        for i in range(num):
            title = "Post " + str(i)
            tags = random.sample(tag_list, random.randint(1, 3))
            Post.create_post(title, s, user.id, tags)


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

    @staticmethod
    def create_comment(name, text='', post_id=0):
        """
        Create a new comment to the database.

        Args:
            name(str): the name of comment.
            text(str): the Content of comment.
            post_id(int): the ID of the post that comment beloings to.
        """
        new_comment = Comment()
        new_comment.name = name
        new_comment.text = text
        new_comment.post_id = post_id
        new_comment.data = datetime.datetime.now()
        db.session.add(new_comment)
        db.session.commit()


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
