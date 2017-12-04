#!/usr/bin/env python
# encoding: utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Required, Length


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
