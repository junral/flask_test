#!/usr/bin/env python
# encoding: utf-8

# import datetime

# from flask_login import AnonymousUserMixin

# from .extensions import bcrypt, mongo

# # 针对非关系性数据 MongoDB 建立的数据库模型
# # MongoDB 是文档式的 NoSQL 数据库，文档被存储在集合（collections）里。文档格式
# # 由叫作 BSON 的格式来定义的，BSON 是 JSON 的超集，意思是二进制的 JSON（Binary
# # JSON）。BSON 允许把 JSON 存为二进制格式，可以节省大量空间。BSON 还有另外几种
# # 不同的存储数值的方式，比如32位整数和双精度数值

# avalidable_roles = ('admin', 'poster', 'defalut')


# class User(mongo.Document):
    # username = mongo.StringField(required=True)
    # password = mongo.StringField(required=True)
    # roles = mongo.ListField(
        # mongo.StringField(choices=avalidable_roles)
    # )

    # def __repr__(self):
        # return "<User '{}'>".format(self.username)

    # def set_password(self, password):
        # self.password = bcrypt.generate_password_hash(password)

    # def check_password(self, password):
        # return bcrypt.check_password_hash(self.password, password)

    # def is_authenicated(self):
        # if isinstance(self, AnonymousUserMixin):
            # return False
        # else:
            # return True

    # def is_active(self):
        # return True

    # def is_anonymous(self):
        # if isinstance(self, AnonymousUserMixin):
            # return True
        # else:
            # return False

    # def get_id(self):
        # return str(self.id)


# class Comment(mongo.EmbeddedDocument):
    # name = mongo.StringField(required=True)
    # text = mongo.StringField(required=True)
    # date = mongo.DateTimeField(
        # default=datetime.datetime.now()
    # )

    # def __repr__(self):
        # return "<Comment '{}'>".format(self.text[:15])


# class Tag(mongo.Document):
    # title = mongo.StringField(required=True)

    # def __repr__(self):
        # return "<Tag '{}'>".format(self.title)


# class Post(mongo.Document):
    # title = mongo.StringField(required=True)
    # # 如果使用下面继承的类，需要删除 text 属性
    # # text = mongo.StringField()
    # publish_date = mongo.DateTimeField(
        # default=datetime.datetime.now()
    # )
    # user = mongo.ReferenceField(User)

    # # 添加文档可以通过 comments.append(comment) 方法添加
    # comments = mongo.ListField(
        # mongo.EmbeddedDocumentField(Comment)
    # )

    # #  多对多关系
    # #  查询操作
    # #  Post.objects(tags__in='Python').all()
    # tags = mongo.ListField(mongo.StringField())

    # def __repr__(self):
        # return "<Post '{}'>".format(self.title)

    # meta = {
        # 'collection': 'user_posts',
        # # 设置文档数量允许的最大值
        # 'max_documents': 10000,
        # # 设定文档大小允许的的最大值
        # 'max_size': 2000000,
        # # 设置索引
        # # 可以是由字符串指定的单字段索引，也可以是有元组指定的多字段索引
        # 'indexes': [
            # 'title',
            # ('title', 'user')
        # ],
        # # 设定默认排序方式
        # # 查询时如果指定了 order_by，则可以覆盖这里设置的缺省行为
        # 'ordering': ['-publish_date'],

        # # 指定自定义文档类型是否允许继承
        # 'allow_inheritance': True
    # }


# #  指定位置类型 可以使用 DynamicField
# #  字段类型实例的可传入参数：
# #  Field(
    # #  # 主键
    # #  # 如果传入该参数，贼表示不希望通过 MongoEngine自动生成唯一标识键，
    # #  # 而采用传入该字段的值作为其 ID
    # #  primary_key=None,

    # #  # 键名
    # #  # 如果没有设置，缺省值就是那个类属性的名字
    # #  db_field=None,

    # #  # 指定该键是否必须存在文档中
    # #  required=False,

    # #  # 指定当该字段赋值时默认返回的默认值
    # #  default=None,

    # #  # 指定是否检查并确保集合中没有其它文档在这个字段有同样的值
    # #  unique=False,

    # #  # 可以接收单个字段或多个字段的列表，它会确保这些字段的值的组合在每个
    # #  # 文档中是唯一的。
    # #  unique_with=None,

    # #  # 传入一个列表，该字段的值将会被限制为只允许从这个列表中选择
    # #  choices=None
# #  )
# #  可以通过定义类从 mongo.DynamicDocument 继承，那么任何额外的字段都会被认为是
# #  DynamicField，并且会被保存到文档中
# #  同时通过下面的定义，可以设定没有必需的字典，而且允许设置任何字段
# #  class Post(mongo.DynamicDocument):
    # #  pass


# class BlogPost(Post):
    # text = mongo.StringField(required=True)

    # @property
    # def type(self):
        # return 'blog'


# class VideoPost(Post):
    # url = mongo.StringField(required=True)

    # @property
    # def type(self):
        # return 'video'


# class ImagePost(Post):
    # image_url = mongo.StringField(required=True)

    # @property
    # def type(self):
        # return 'image'


# class QuotePost(Post):
    # quote = mongo.StringField(required=True)
    # author = mongo.StringField(required=True)

    # @property
    # def type(self):
        # return 'quote'
