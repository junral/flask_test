#!/usr/bin/env python
# encoding: utf-8

from flask import Flask
from flask import redirect, url_for
from flask_bootstrap import Bootstrap

from .models import db
from .config import config

bootstrap = Bootstrap()


def create_app(object_name):
    """
    工厂函数：用于产生 app
    """
    app = Flask(__name__)
    app.config.from_object(config[object_name])

    bootstrap.init_app(app)
    db.init_app(app)

    @app.route('/')
    def index():
        return redirect(url_for('blog.home'))

    from .controllers.blog import blog_blueprint
    app.register_blueprint(blog_blueprint)

    return app
