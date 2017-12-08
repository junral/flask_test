#!/usr/bin/env python
# encoding: utf-8

# import datetime

from flask import abort
from flask_restful import Resource, fields, marshal_with

from .fields import HTMLField
from .parsers import post_get_parser, post_post_parser, post_put_parser, \
    Post_delete_parser

from ...models import Post, Tag, User
# from ...extensions import db

#  Flask Restful 提供的多种默认字段：
#  fields.String: 会使用 str() 对值进行转换
#  fields.FormattedString: 接受 Python 中的格式字符串，变量名包括高大括号中
#  fields.Url: 跟 Flask 中的 url_for 功能一样
#  fields.DateTime: 把 Python 的data或者 datetime 对象转换成字符串
#  关键字参数format 之赐你个了应该使用 ISO8601 还是 RFC822 规范来格式化
#  fields.Float: 将值转换成以字符串表示的浮点数
#  fields.Integer: 将值转换成以字符串表示的整数
#  fields.Nested: 允许通过其他字段对象构成的字典来格式化嵌套的对象
#  fields.List: 很像 MongoEngine 中的 API，这个字段接收另一种字段类型作为参数，
#  尝试将值的列表转换成该字段类型的 JSON 列表
#  fields.Boolean: 将值转换以字符串表示的布尔类型

# 自定义字段集合
nested_tag_fields = {
    'id': fields.Integer(),
    'title': fields.String()
}

post_fields = {
    'author': fields.String(attribute=lambda x: x.user.username),
    'title': fields.String(),
    'text': HTMLField(),
    'tags': fields.List(fields.Nested(nested_tag_fields)),
    'publish_date': fields.DateTime(dt_format='iso8601')
}


class PostApi(Resource):
    @marshal_with(post_fields)
    def get(self, post_id=None):
        if post_id:
            post = Post.query.get(post_id)
            if not post:
                abort(404)

            return post
        else:
            #  posts = Post.query.all()
            #  return posts
            args = post_get_parser.parse_args()
            page = args['page'] or 1

            if args['user']:
                user = User.query.filter_by(
                    username=args['user']
                ).first()

                posts = user.query.order_by(
                    Post.publish_date.desc()
                ).paginate(page, 30)
            else:
                posts = Post.query.order_by(
                    Post.publish_date.desc()
                ).paginate(page, 30)

            return posts.items

    def post(self, post_id=None):
        if post_id:
            abort(405)
        else:
            args = post_post_parser.parse_args(strict=True)

            user = User.verify_auth_token(args['token'])
            if not user:
                abort(401)

            #  new_post = Post(args['title'])
            #  new_post.date = datetime.datetime.now()
            #  new_post.text = args['text']
            #  new_post.user = user

            #  if args['tags']:
            #  for item in args['tags']:
            #  tag = Tag.query.filter_by(name=item).first()

                    #  #  如果存在该标签，就添加
                    #  #  如果不存在，就先创建再添加
                    #  if tag:
                    #  new_post.tags.append(tag)
                    #  else:
                    #  new_tag = Tag(item)
                    #  new_post.tags.append(new_tag)

                #  db.session.add(new_post)
                #  db.session.commit()

            tags = [Tag.create(tag)
                    for tag in args['tags']
                    if args['tags']]
            new_post = Post.create(
                args['title'],
                args['text'],
                user,
                tags
            )
            return new_post.id, 201

        def put(self, post_id=None):
            if not post_id:
                abort(404)

            post = Post.query.get(post_id)

            if not post:
                abort(404)

            args = post_put_parser.parse_args(strice=True)
            user = User.verify_auth_token(args['token'])
            if not user:
                abort(401)
            if user != post.user:
                abort(403)

            #  if args['title']:
                #  post.title = args['title']

            #  if args['text']:
                #  post.title = args['text']

            #  if args['tags']:
            #  for item in args['tags']:
            #  tag = Tag.query.filter_by(name=item).first()

                    #  #  标签若存在则添加：
                    #  #  如果不存在则创建并添加
                    #  if tag:
                    #  post.tags.append(tag)
                    #  else:
                    #  new_tag = Tag(item)
                    #  post.tags.append(new_tag)

            #  db.session.add(post)
            #  db.session.commit()

            tags = [Tag.create(tag)
                    for tag in args['tags']
                    if args['tags']]
            post.change(args['title'], args['text'], tags)

            return post.id, 201

        def delete(self, post_id=None):
            if not post_id:
                abort(400)

            post = Post.query.get(post_id)
            if not post:
                abort(404)

            args = Post_delete_parser.parse_args(strice=True)
            user = User.verify_auth_token(args['token'])
            if user != post.user:
                abort(403)

            #  db.session.delete(post)
            #  db.session.comit()
            post.delete()
            return '', 204
