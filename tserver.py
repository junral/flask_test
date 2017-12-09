#!/usr/bin/env python
# coding: utf-8

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from webapp import create_app

app = WSGIContainer(create_app('prod'))
http_server = HTTPServer(app)
# 绑定端口号
http_server.listen(80)
IOLoop.instance().start()
