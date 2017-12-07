#!/usr/bin/env python
# encoding: utf-8

from flask_admin import (
    BaseView,
    #  FileAdmin,
    expose
)
# 使用的是 SQLAlchemy：
from flask_admin.contrib.sqla import ModelView
# 如果使用的是 MongoEngine：
# from flask_admin.contrib.mongoengine import ModelView
from flask_login import (
    login_required,
    # AnonymousUser,
    current_user
)

from ..forms import CKTextAreaField
from ..extensions import admin_permission


class CustomView(BaseView):
    @expose('/')
    @login_required
    @admin_permission.require(http_exception=403)
    def index(self):
        return self.render('admin/custom.html')

    @expose('/second_page')
    @login_required
    @admin_permission.require(http_exception=403)
    def second_page(self):
        return self.render('admin/second_page.html')


class CustomModelView(ModelView):
    # pass
    def is_accessible(self):
        # 设置管理员访问权限
        return current_user.is_authenticated() and admin_permission.can()


class PostView(CustomModelView):
    form_overrides = dict(text=CKTextAreaField)
    column_searchable_title = ('text', 'title')
    column_filters = ('publish_date',)

    create_template = 'admin/post_edit.html'
    edit_template = 'admin/post_edit.html'


#  class CustomFileAdmin(FileAdmin):
    #  def is_accessible(self):
    #  return current_user.is_authenicated() and admin_permission.can()
