#!/usr/bin/env python
# encoding: utf-8

from flask_restful import reqparse

# add_argument() 方法参数说明：
# action: 生命了当参数值成功传入后，解释器进入哪种后继操作。两个可选项是 store 和
# append。store 会把解析后的值加到返回的字典中，append 会把解析后的值加到了一个
# 列表中，并加入返回的字典
# case_sensitive: 布尔值，声明该参数名是否大小写敏感
# choices: 跟MongoEngine 类似，提供一个可选值的列表。
# default: 该参数没有传入时生成的默认值
# dest: 加入返回的字典所使用的键名
# help: 如果参数不符合要求，则会像用户显示此信息
# ignore: 布尔值，声明当类型检查失败时是否返回错误
# location: 指出应该从哪里寻找所需要的数据。可用的选项如下：
    # args: 在 GET 参数字符串中查找
    # headers: 在 HTTP 请求头中查找
    # form: 在HTPP的 POST 表单数据中查找
    # cookies: 在 HTTP 的 cookie 中查找
    # files: 在 POST 的文件域中查找
# required: 布尔值，声明该参数是否可选
# store_missing: 布尔值，当请求中缺失该参数时是否使用默认值进行填充
# type: 把传入的参数值转换成那种 Python 类型

post_get_parser = reqparse.RequestParser()
post_get_parser.add_argument(
    'page',
    type=int,
    location=['join', 'args', 'headers']
)

post_get_parser.add_argument(
    'user',
    type=str,
    location=['join', 'args', 'headers']
)

post_post_parser = reqparse.RequestParser()
post_post_parser.add_argument(
    'title',
    type=str,
    required=True,
    help="Title is required"
)

post_post_parser.add_argument(
    'text',
    type=str,
    required=True,
    help="Body text is required"
)

post_post_parser.add_argument(
    'token',
    type=str,
    required=True,
    help="Auth Token is required to add posts"
)

post_post_parser.add_argument(
    'tags',
    type=str,
    action='append'
)

post_put_parser = reqparse.RequestParser()
post_put_parser.add_argument(
    'token',
    type=str,
    help='Auth Token is required to edit posts'
)

post_put_parser.add_argument(
    'title',
    type=str
)

post_put_parser.add_argument(
    'text',
    type=str
)

post_put_parser.add_argument(
    'tags',
    type=str,
    action='append'
)

Post_delete_parser = reqparse.RequestParser()
Post_delete_parser.add_argument(
    'token',
    type=str,
    required=True,
    help="Auth Token is required to delete posts"
)

user_post_parser = reqparse.RequestParser()
user_post_parser.add_argument(
    'username',
    type=str,
    required=True
)

user_post_parser.add_argument(
    'password',
    type=str,
    required=True
)
