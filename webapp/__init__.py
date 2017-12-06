#!/usr/bin/env python
# encoding: utf-8

from flask import Flask
from flask_login import current_user
from flask_principal import identity_loaded, UserNeed, RoleNeed

from .extensions import bootstrap, db, bcrypt, oid, login_manager, principals
from .extensions import mongo, rest_api
# from .extensions import oauth
from .config import config
from .controllers.rest.post import PostApi
from .controllers.rest.auth import AuthApi


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
    login_manager.init_app(app)
    principals.init_app(app)
    mongo.init_app(app)
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

    from .controllers.main import main_blueprint
    app.register_blueprint(main_blueprint)

    from .controllers.blog_mongo import blog_mongo_blueprint
    app.register_blueprint(blog_mongo_blueprint)

    from .controllers.main_mongo import main_mongo_blueprint
    app.register_blueprint(main_mongo_blueprint)

    return app
