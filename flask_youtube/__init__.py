#!/usr/bin/env python
# encoding: utf-8

from flask import (
    flash,
    redirect,
    url_for,
    session,
    render_template,
    Blueprint,
    Markup
)


class Youtube(object):
    """
    一个 YouTube 的 Flask 扩展。
    """
    def __init__(self, app=None, **kwargs):
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.register_blueprint(app)
        # 添加 HTML 模板
        app.add_template_global(youtube)

    def register_blueprint(self, app):
        module = Blueprint(
            'youtube',
            __name__,
            template_folder="templates"
        )
        app.register_blueprint(module)
        return module


class Video(object):
    """
    用于描述嵌入的视频。
    处理从 Jinja 传入的参数，并渲染一段 HTML 显示在模板里
    """
    def __init__(self, video_id, cls="youtube"):
        self.video_id = video_id
        self.cls = cls

    def render(self, *args, **kwargs):
        return render_template(*args, **kwargs)

    @property
    def html(self):
        return Markup(
            self.render(
                'youtube/video.html',
                video=self
            )
        )


def youtube(*args, **kwargs):
    video = Video(*args, **kwargs)
    return video.html

youtube_ext = Youtube()


