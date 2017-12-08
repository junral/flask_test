#!/usr/bin/env python
# encoding: utf-8

import os

from webapp import create_app
from webapp.tasks import log
from celery import Celery


def make_celery(app):
    """
    把每个对 celery 任务的调用，都包含到一个 Python
    的 with 代码块中，这样就可以确保代码对每个 Falsk
    扩展的调用都会正常工作。
    """
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        #  backend=app.config['CELERY_BACKEND_URL']
        backend=app.config['CELERY_RESULT_BACKEND']
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstrace = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery

env = os.environ.get('WEBAPP', 'default')
flask_app = create_app(env)
celery = make_celery(flask_app)

# 通过使用 celery 命令运行此文件
# 执行下面的命令：
# celery worker -A celery_runner --loglevel=info

# 如果要运行定期任务，需要另外启动一个叫作 beat 的工作进程
# 执行下面的命令：
# celery -A celery_runner beat

# Celery 提供了一下命令行参数来监控 Celery 工作进程和任务
# 这些命令的形式如下：
# celery -A celery_runner <command>
# 主要命令，用于查看工作进程的状态
    #  status：会打印正在运行的工作进程的状态
    #  result：传入一个任务 id，会显示这个任务的返回值及最终的状态
    #  purge：使用这个命令会删除中间人的所有消息
    #  inspect active：列出所有当前正在执行的任务
    #  inspect scheduled：列出所有使用 eta 参数进行排期中的任务
    #  inspece registered：列出所有等待被执行的任务
    #  inspect stats：返回一个字典，包含了当前正在跑的工作进程和中间人的统计信息
