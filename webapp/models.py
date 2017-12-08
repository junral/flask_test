#!/usr/bin/env python
# encoding: utf-8

import datetime

from flask import current_app
from flask_login import AnonymousUserMixin
from sqlalchemy.sql.expression import or_
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired

from .extensions import (
    db,
    #  bcrypt,
    cache
)


# 针对 关系型数据库建立的模型
# 模型 models
roles = db.Table(
    'role_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

# 针对 Post 表和 Tag 表的多对多关系管理
tags = db.Table(
    'tags',
    db.Column('post_id', db.Integer(), db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer(), db.ForeignKey('tag.id'))
)


class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Role '{}'>".format(self.name)

    @staticmethod
    def create_role(name, description=''):
        role = Role.query.filter_by(name=name).first()
        if role is None:
            role = Role(name=name)
            role.description = description
            db.session.add(role)
            db.session.commit()

        return role

    @staticmethod
    def create_roles(role_list):
        if role_list is None:
            return
        for r in role_list:
            if isinstance(r, (tuple, list, set)):
                n, d = r
            else:
                n, d = r, ''
            Role.create_role(n, d)


class User(db.Model):
    """ 用户表 """

    # 数据库表
    __tablename__ = 'user'

    # 主键
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    # 在 SQLAlchem 中创建虚拟的列，和 Post 表中的外键建立联系
    posts = db.relationship(
        'Post',
        backref='user',
        lazy='dynamic'
    )
    comments = db.relationship(
        'Comment',
        backref='user',
        lazy='dynamic'
    )
    roles = db.relationship(
        'Role',
        secondary=roles,
        backref=db.backref('users', lazy='dynamic')
    )

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        default = Role.query.filter_by(name='default').first()
        if default is None:
            default = Role.create_role('default', 'default')
        self.roles.append(default)

    def __repr__(self):
        return r"<User '{}'>".format(self.username)

    def set_password(self, password):
        # self.password = bcrypt.generate_password_hash(password)
        self.password = generate_password_hash(password)

    def check_password(self, password):
        # return bcrypt.check_password_hash(self.password, password)
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return str(self.id)

    def generate_reset_token(self, expiration=3600):
        s = Serializer(
            current_app.config['SECRET_KEY'],
            expiration
        )
        return s.dumps({'reset': self.id})

    def reset_password(self, token, password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return False
        except BadSignature:
            return False

        if self.id != data.get('reset'):
            return False

        self.set_password(password)
        db.session.add(self)
        return True

    def generate_auth_token(self, expiration):
        s = Serializer(
            current_app.config['SECRET_KEY'],
            expiration
        )

        return s.dumps({'id': self.id}).decode('ascii')
        #  return {'token': s.dumps({'id': self.id})}

    @staticmethod
    # 不但会存储函数的运行结果，也会存储调用的参数
    @cache.memoize(60)
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None

        return User.query.get(data['id'])

    @staticmethod
    def create(username='', email='', password=None, roles=None):
        """
        Create a new user.

        Args:
            username(str): the name of user
            email(str): the email of user
            password(str): the password of user
        """
        if not username and not email:
            return None

        user = User.query.filter(
            or_(email == email),
            username == username
        ).first()

        if user is None:
            user = User()
            user.username = username
            user.email = email
            if password is not None:
                user.set_password(password)

            if roles is not None:
                if isinstance(roles, (tuple, list, set)):
                    for role in roles:
                        if role not in user.roles:
                            user.roles.append(role)
                else:
                    user.roles.append(roles)

            db.session.add(user)
            db.session.commit()

        return user


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

    def is_authenticated(self):
        return False


class Post(db.Model):
    """ 博客文章表 """
    __tablename__ = 'post'

    # 主键
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime())
    update_date = db.Column(db.DateTime())
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

    def change(self, title, text='', *tags):
        """
        Chang the post data.

        Args:
            title(str): the title of the psot.
            Text(str): the content of the psot.
            *tags: a set of tag.
        """
        if title:
            self.title = title
        if text:
            self.text = text
        self.publish_date = datetime.datetime.now()
        self.tags.extend(*tags)
        db.session.add(self)

        # self.update(
        # {
        # 'title': title,
        # 'text': text,
        # 'update_date': datetime.datetime.now()
        # }
        # )

        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def create(title, text='', user_id=0, *tags):
        """
        Create a new post to database.

        Args:
            title(str): the title of the psot.
            Text(str): the content of the psot.
            user_id(int): the ID of user who the post belongs to.
            *tags: a set of tag.
        """
        if not title:
            return None

        new_post = Post(title)
        new_post.text = text
        new_post.publish_date = datetime.datetime.now()
        #  new_post.user = user
        new_post.user_id = user_id
        new_post.tags.extend(*tags)
        db.session.add(new_post)
        db.session.commit()
        return new_post

    @staticmethod
    def generate_fake_posts(num=100):
        """
        Generate some test datas with tags.

        Args:
            num: the numbers of the data want to generate.
        """
        import random
        user = User.query.get(1)
        tag_list = [Tag.create(tag)
                    for tag in ('Python', 'Flask', 'SQLAlchemy', 'Jinja')]

        s = "Example text"

        for i in range(num):
            title = "Post " + str(i)
            tags = random.sample(tag_list, random.randint(1, 3))
            Post.create(title, s, user.id, tags)


class Comment(db.Model):
    """ 评论表 """
    __tablename__ = 'comment'

    # 主键
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    text = db.Column(db.Text())
    date = db.Column(db.DateTime())
    # 外键
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'))

    def __repr__(self):
        return "<Comment '{}'>".format(self.text[:15])

    @staticmethod
    def create(name, text='', post_id=0, user_id=0):
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
        #  new_comment.post = post
        #  new_comment.user = user
        new_comment.post_id = post_id
        new_comment.user_id = user_id
        new_comment.data = datetime.datetime.now()
        db.session.add(new_comment)
        db.session.commit()

        return new_comment


class Tag(db.Model):
    """ 标签表 """
    __tablename__ = 'tag'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Tag '{}'>".format(self.name)

    @staticmethod
    def create(name):
        tag = Tag.query.filter_by(name=name).first()
        if tag is None:
            tag = Tag(name=name)
            db.session.add(tag)
            db.session.commit()

        return tag

    @staticmethod
    def create_tags(tag_list):
        for t in tag_list:
            Tag.create(t)


# 创建提醒应用的相关模型：
class Reminder(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.DateTime())
    email = db.Column(db.String())
    text = db.Column(db.Text())

    def __repr__(self):
        return "<Reminder '{}'>".format(self.text[:20])
