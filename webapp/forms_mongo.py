#!/usr/bin/env python
# encoding: utf-8

# from flask_wtf import FlaskForm
# from wtforms import StringField, TextAreaField, PasswordField, SubmitField, SelectField
# from wtforms import BooleanField
# from wtforms.validators import Required, Length, EqualTo, Email, URL

# from .models_mongo import User


# # 配合 MongoDB 定义的数据模型使用
# class CommentForm(FlaskForm):
    # """ 评论的表单 """
    # name = StringField(
        # 'Name', validators=[Required(), Length(max=255)]
    # )

    # text = TextAreaField(
        # 'Comment', validators=[Required()]
    # )
    # # submit = SubmitField('Add Comment')


# class LoginForm(FlaskForm):
    # """ 用户登录表单 """
    # username = StringField(
        # 'Username', [Required(), Length(max=255)]
    # )

    # password = PasswordField(
        # 'Password', [Required()]
    # )
    # remember = BooleanField('Remember Me')

    # def validators(self):
        # check_validate = super(LoginForm, self).validate()

        # # 如果验证没有通过
        # if not check_validate:
            # return False

        # # 检查是否存在该用户
        # user = User.objects(
            # username=self.username.data).first()
        # if not user:
            # self.username.errors.append(
                # 'Invalid username or password')
            # return False

        # # 检查密码是否匹配
        # if not self.user.check_password(self.password.data):
            # self.username.errors.append(
                # 'Invalid username or password'
            # )
            # return False

        # return True


# class RegisterForm(FlaskForm):
    # """ 用户注册表单 """
    # username = StringField(
        # 'Username',
        # [Required(), Length(max=255)]
    # )

    # email = StringField(
        # 'Email',
        # [Required(), Length(max=255), Email()]
    # )

    # password = PasswordField(
        # 'Password',
        # [Required(), Length(min=8)]
    # )

    # confrim = PasswordField(
        # 'Confirm Password',
        # [Required(), EqualTo('password')]
    # )

    # submit = SubmitField('Register')

    # # recaptcha = RecaptchaField()

    # def validates(self):
        # check_validate = super(RegisterForm, self).validate()

        # # 如果验证没有通过
        # if not check_validate:
            # return False

        # # 检查用户名是否已存在
        # user = User.objects(username=self.username.data).first()
        # if not user:
            # self.username.errors.append('User with that name already exists')
            # return False

        # # 检查用户邮箱是否已存在
        # user = User.objects(email=self.email.data).first()
        # if not user:
            # self.username.errors.append('User with that email already exists')
            # return False

        # return True


# class PostForm(FlaskForm):
    # """ 文章表单 """
    # title = StringField('Title', [Required(), Length(max=255)])
    # type = SelectField('Post Type', choices=[
        # ('blog', 'Blog Post'),
        # ('image', 'Image'),
        # ('video', 'Video'),
        # ('quote', 'Quote')
    # ])
    # text = TextAreaField('Content')
    # image = StringField('Image URL', [URL(), Length(max=255)])
    # video = StringField('Video Code', [URL(), Length(max=255)])
    # author = StringField('Author', [URL(), Length(max=255)])


# class OpenIDForm(FlaskForm):
    # openid = StringField('OpenID URL', [Required(), URL()])


# def custom_email(form, field):
    # """ 自定义表单邮箱验证 """
    # import re
    # import wtforms
    # if not re.match(r'[^@]+@[^@]+\.[^@]+', field.data):
        # raise wtforms.ValidationError('Field must be a valid email address.')
