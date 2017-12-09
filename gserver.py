#!/usr/bin/env python
# coding: utf-8

from gevent.wsgi import WSGIServer

from webapp import create_app

app = create_app('prod')
# bind the host and port
server = WSGIServer(('', 80), app)
