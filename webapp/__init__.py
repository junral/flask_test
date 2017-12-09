#!/usr/bin/env python
# encoding: utf-8

#  import os

from flask import Flask
from flask_login import current_user
from flask_principal import identity_loaded, UserNeed, RoleNeed
from sqlalchemy import event

from .extensions import (
    bootstrap,
    db,
    bcrypt,
    oid,
    login_manager,
    principals,
    mongo,
    rest_api,
    celery,
    debug_toolbar,
    cache,
    assets_env,
    main_js,
    main_css,
    admin,
    mail,
    # youtube_ext,
    babel
)
#  from .extensions import oauth
from .config import config
from .controllers.rest.post import PostApi
from .controllers.rest.auth import AuthApi
from .models import (
    User, Role, Post, Comment, Tag, Reminder, AnonymousUser
)
from .tasks import on_reminder_save
from .controllers.admin import (
    CustomView,
    #  CustomFileAdmin,
    PostView,
    CustomModelView
)


def create_app(object_name):
    """
    工厂函数：用于生成 app
    """
    app = Flask(__name__)
    app.config.from_object(config[object_name])

    bootstrap.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)
    oid.init_app(app)
    # oauth.init_app(app)
    login_manager.anonymous_user = AnonymousUser
    login_manager.login_view = 'auth.login'
    # login_manager.login_view = 'main_mongo.login'
    login_manager.session_protection = 'strong'
    login_manager.login_message = 'Please login to access this page'
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)
    principals.init_app(app)
    mongo.init_app(app)
    event.listen(
        Reminder,
        'after_insert',
        on_reminder_save
    )
    rest_api.add_resource(
        PostApi,
        '/api/post',
        '/api/post/<int:post_id>',
        endpoint='api'
    )
    rest_api.add_resource(
        AuthApi,
        '/api/auth'
    )
    rest_api.init_app(app)
    celery.init_app(app)
    debug_toolbar.init_app(app)
    cache.init_app(app)
    assets_env.init_app(app)
    assets_env.register('main_js', main_js)
    assets_env.register('main_css', main_css)
    admin.init_app(app)
    admin.add_view(CustomView(name='Custom'))
    models = [User, Role, Post, Comment, Tag, Reminder]

    for model in models:
        admin.add_view(
            CustomModelView(
                model,
                db.session,
                category='models'
            )
        )

    #  admin.add_view(
        #  PostView(
            #  Post,
            #  db.session,
            #  category='PostsAdmin'
        #  )
    #  )

    #  admin.add_view(
        #  CustomFileAdmin(
            #  os.path.join(os.path.dirname(__file__), 'static'),
            #  '/static/',
            #  name='Static Files'
        #  )
    #  )

    mail.init_app(app)
    babel.init_app(app)
    # youtube_ext.init_app(app)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        # set the identity user object
        identity.user = current_user

        # Add the UserNeed to the identity
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        # Add each role to the identity
        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))

    from .controllers.blog import blog_blueprint
    app.register_blueprint(blog_blueprint)

    from .controllers.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    # from .controllers.blog_mongo import blog_mongo_blueprint
    # app.register_blueprint(blog_mongo_blueprint)

    # from .controllers.auth_mongo import auth_mongo_blueprint
    # app.register_blueprint(auth_mongo_blueprint)

    return app
